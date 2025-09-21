from __future__ import annotations
import typing as T
from jsonschema import Draft202012Validator
_CEFR = ["A1", "A2", "B1", "B2", "C1", "C2", "native", ""]

STRUCTURED_RESUME_SCHEMA: T.Dict[str, T.Any] = {
  "type": "object",
  "properties": {
    "name": {"type": "string"},
    "surname": {"type": "string"},
    "gender": {"type": "string", "enum": ["Male", "Female", ""]},
    "age": {"type": ["integer", "null"]},
    "date_of_birth": {"type": "string"},
    "summary": {"type": "string"},

    "contacts": {
      "type": "object",
      "properties": {
        "emails": {"type": "array", "items": {"type": "string"}},
        "phones": {"type": "array", "items": {"type": "string"}},
        "urls":   {"type": "array", "items": {"type": "string"}}
      },
      "required": ["emails", "phones", "urls"],
      "additionalProperties": False
    },

    "education": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "institution": {"type": "string"},
          "degree": {"type": "string"},
          "field": {"type": "string"},
          "location": {"type": "string"},
          "start": {"type": "string"},
          "end": {"type": "string"},
          "period": {"type": "string"},
          "status": {"type": "string"}
        },
        "additionalProperties": False
      }
    },

    "experience": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "company": {"type": "string"},
          "position": {"type": "string"},
          "role": {"type": "string"},
          "location": {"type": "string"},
          "start": {"type": "string"},
          "end": {"type": "string"},
          "period": {"type": "string"},
          "description": {"type": "string"},
          "responsibilities": {"type": "array", "items": {"type": "string"}}
        },
        "additionalProperties": False
      }
    },

    "skills": {
      "type": "object",
      "properties": {
        "hard": {"type":"array","items":{"type":"string"}},
        "soft": {"type":"array","items":{"type":"string"}}
      },
      "required": ["hard","soft"],
      "additionalProperties": False
    },

    "languages": {
      "type":"array",
      "items":{
        "oneOf": [
          {
            "type":"object",
            "properties":{"language":{"type":"string"},"level":{"type":"string","enum": _CEFR}},
            "required":["language","level"],
            "additionalProperties": False
          },
          {
            "type":"object",
            "properties":{
              "language":{"type":"string"},
              "listening":{"type":"string","enum": _CEFR},
              "reading":{"type":"string","enum": _CEFR},
              "spoken_production":{"type":"string","enum": _CEFR},
              "spoken_interaction":{"type":"string","enum": _CEFR},
              "writing":{"type":"string","enum": _CEFR}
            },
            "required":["language"],
            "additionalProperties": False
          }
        ]
      }
    },

    "projects": {
      "type":"array",
      "items":{
        "type":"object",
        "properties":{
          "name":{"type":"string"},
          "description":{"type":"string"},
          "link":{"type":"string"}
        },
        "additionalProperties": False
      }
    },

    "awards": {
      "type":"array",
      "items":{
        "type":"object",
        "properties":{
          "title":{"type":"string"},
          "award":{"type":"string"},
          "issuer":{"type":"string"},
          "date":{"type":"string"},
          "description":{"type":"string"}
        },
        "additionalProperties": False
      }
    },

    "hobbies": {"type":"array","items":{"type":"string"}},

    "request": {
      "type":"object",
      "properties":{
        "type": {"type":"string", "enum":["resume","tags","classification","embeddings"]},
        "format": {"type":"string", "enum":["json"]},
        "model": {"type":"string"}
      },
      "required": ["type","format","model"],
      "additionalProperties": False
    }
  },

  "required": ["contacts","skills","request"],
  "additionalProperties": False
}

def ensure_valid_resume(obj: dict) -> None:
    Draft202012Validator(STRUCTURED_RESUME_SCHEMA).validate(obj)