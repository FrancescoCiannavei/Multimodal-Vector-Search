package server

import (
	"encoding/json"
	"html/template"
	"net/http"

	"Multimodal-Vector-Search/internal/static"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/go-chi/cors"
)

func (s *Server) RegisterRoutes() http.Handler {
	r := chi.NewRouter()
	r.Use(middleware.Logger)

	r.Use(cors.Handler(cors.Options{
		AllowedOrigins:   []string{"https://*", "http://*"},
		AllowedMethods:   []string{"GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"},
		AllowedHeaders:   []string{"Accept", "Authorization", "Content-Type"},
		AllowCredentials: true,
		MaxAge:           300,
	}))

	r.Get("/", s.HomeHandler)
	r.Get("/health", s.healthHandler)

	r.Handle("/html/*", http.FileServerFS(static.Files))
	r.Handle("/js/*", http.FileServerFS(static.Files))
	r.Handle("/css/*", http.FileServerFS(static.Files))

	return r
}

func (s *Server) HomeHandler(w http.ResponseWriter, r *http.Request) {
	var homeTmpl = template.Must(template.ParseFS(static.Files, "html/index.html"))
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	data := struct{ Title, Heading string }{"Home", "test"}
	if err := homeTmpl.Execute(w, data); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}

func (s *Server) healthHandler(w http.ResponseWriter, r *http.Request) {
	jsonResp, _ := json.Marshal(s.db.Health())
	_, _ = w.Write(jsonResp)
}
