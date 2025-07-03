"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

interface Entity {
  id: string
  name: string
  type: "person" | "company" | "project" | "location"
  x: number
  y: number
}

interface Relationship {
  from: string
  to: string
  label: string
  type: "works_at" | "friends_with" | "collaborates_on" | "located_in" | "manages"
}

const entities: Entity[] = [
  { id: "alice", name: "Alice Johnson", type: "person", x: 150, y: 100 },
  { id: "bob", name: "Bob Smith", type: "person", x: 350, y: 150 },
  { id: "carol", name: "Carol Davis", type: "person", x: 250, y: 250 },
  { id: "techcorp", name: "TechCorp", type: "company", x: 150, y: 300 },
  { id: "webapp", name: "Web App Project", type: "project", x: 450, y: 200 },
  { id: "seattle", name: "Seattle", type: "location", x: 50, y: 200 },
]

const relationships: Relationship[] = [
  { from: "alice", to: "techcorp", label: "works at", type: "works_at" },
  { from: "bob", to: "techcorp", label: "works at", type: "works_at" },
  { from: "alice", to: "bob", label: "friends with", type: "friends_with" },
  { from: "bob", to: "webapp", label: "collaborates on", type: "collaborates_on" },
  { from: "carol", to: "webapp", label: "manages", type: "manages" },
  { from: "alice", to: "seattle", label: "located in", type: "located_in" },
  { from: "techcorp", to: "seattle", label: "located in", type: "located_in" },
]

const getEntityColor = (type: Entity["type"]) => {
  switch (type) {
    case "person":
      return "bg-blue-100 border-blue-300 text-blue-800"
    case "company":
      return "bg-green-100 border-green-300 text-green-800"
    case "project":
      return "bg-purple-100 border-purple-300 text-purple-800"
    case "location":
      return "bg-orange-100 border-orange-300 text-orange-800"
    default:
      return "bg-gray-100 border-gray-300 text-gray-800"
  }
}

const getRelationshipColor = (type: Relationship["type"]) => {
  switch (type) {
    case "works_at":
      return "stroke-green-500"
    case "friends_with":
      return "stroke-blue-500"
    case "collaborates_on":
      return "stroke-purple-500"
    case "located_in":
      return "stroke-orange-500"
    case "manages":
      return "stroke-red-500"
    default:
      return "stroke-gray-400"
  }
}

export default function GComponent() {
  const [selectedEntity, setSelectedEntity] = useState<string | null>(null)
  const [hoveredRelation, setHoveredRelation] = useState<string | null>(null)

  const getConnectedEntities = (entityId: string) => {
    return relationships
      .filter((rel) => rel.from === entityId || rel.to === entityId)
      .map((rel) => (rel.from === entityId ? rel.to : rel.from))
  }

  return (
    <div className="w-full max-w-4xl mx-auto p-4">
      <Card>
        <CardHeader>
          <CardTitle>Entity Relationship Graph</CardTitle>
          <div className="flex flex-wrap gap-2">
            <Badge variant="outline" className="bg-blue-50">
              <div className="w-2 h-2 bg-blue-500 rounded-full mr-2"></div>
              Person
            </Badge>
            <Badge variant="outline" className="bg-green-50">
              <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
              Company
            </Badge>
            <Badge variant="outline" className="bg-purple-50">
              <div className="w-2 h-2 bg-purple-500 rounded-full mr-2"></div>
              Project
            </Badge>
            <Badge variant="outline" className="bg-orange-50">
              <div className="w-2 h-2 bg-orange-500 rounded-full mr-2"></div>
              Location
            </Badge>
          </div>
        </CardHeader>
        <CardContent>
          <div className="relative">
            <svg width="500" height="400" className="border rounded-lg bg-gray-50">
              {/* Render relationships (edges) */}
              {relationships.map((rel, index) => {
                const fromEntity = entities.find((e) => e.id === rel.from)
                const toEntity = entities.find((e) => e.id === rel.to)

                if (!fromEntity || !toEntity) return null

                const isHighlighted = selectedEntity && (rel.from === selectedEntity || rel.to === selectedEntity)

                const relationKey = `${rel.from}-${rel.to}`

                return (
                  <g key={index}>
                    <line
                      x1={fromEntity.x}
                      y1={fromEntity.y}
                      x2={toEntity.x}
                      y2={toEntity.y}
                      className={`${getRelationshipColor(rel.type)} ${
                        isHighlighted ? "stroke-2" : "stroke-1"
                      } ${hoveredRelation === relationKey ? "stroke-2" : ""}`}
                      strokeDasharray={rel.type === "friends_with" ? "5,5" : "none"}
                      onMouseEnter={() => setHoveredRelation(relationKey)}
                      onMouseLeave={() => setHoveredRelation(null)}
                    />
                    {/* Relationship label */}
                    <text
                      x={(fromEntity.x + toEntity.x) / 2}
                      y={(fromEntity.y + toEntity.y) / 2 - 5}
                      className="text-xs fill-gray-600 text-center"
                      textAnchor="middle"
                      style={{
                        opacity: hoveredRelation === relationKey ? 1 : 0.7,
                        fontSize: "10px",
                      }}
                    >
                      {rel.label}
                    </text>
                  </g>
                )
              })}

              {/* Render entities (nodes) */}
              {entities.map((entity) => {
                const isSelected = selectedEntity === entity.id
                const isConnected = selectedEntity && getConnectedEntities(selectedEntity).includes(entity.id)

                return (
                  <g key={entity.id}>
                    <circle
                      cx={entity.x}
                      cy={entity.y}
                      r={isSelected ? 25 : 20}
                      className={`${getEntityColor(entity.type)} cursor-pointer transition-all duration-200 ${
                        isSelected ? "ring-2 ring-offset-2 ring-blue-500" : ""
                      } ${isConnected ? "ring-1 ring-blue-300" : ""}`}
                      onClick={() => setSelectedEntity(selectedEntity === entity.id ? null : entity.id)}
                      style={{
                        filter: selectedEntity && !isSelected && !isConnected ? "opacity(0.3)" : "opacity(1)",
                      }}
                    />
                    <text
                      x={entity.x}
                      y={entity.y + 35}
                      className="text-xs font-medium text-center fill-gray-700"
                      textAnchor="middle"
                      style={{ maxWidth: "80px" }}
                    >
                      {entity.name}
                    </text>
                  </g>
                )
              })}
            </svg>

            {/* Entity details panel */}
            {selectedEntity && (
              <div className="mt-4 p-4 bg-blue-50 rounded-lg border">
                <h3 className="font-semibold text-blue-900">{entities.find((e) => e.id === selectedEntity)?.name}</h3>
                <p className="text-sm text-blue-700 mb-2">
                  Type: {entities.find((e) => e.id === selectedEntity)?.type}
                </p>
                <div>
                  <p className="text-sm font-medium text-blue-900 mb-1">Connected to:</p>
                  <div className="flex flex-wrap gap-1">
                    {getConnectedEntities(selectedEntity).map((connectedId) => {
                      const connectedEntity = entities.find((e) => e.id === connectedId)
                      const relationship = relationships.find(
                        (r) =>
                          (r.from === selectedEntity && r.to === connectedId) ||
                          (r.to === selectedEntity && r.from === connectedId),
                      )
                      return (
                        <Badge key={connectedId} variant="secondary" className="text-xs">
                          {connectedEntity?.name} ({relationship?.label})
                        </Badge>
                      )
                    })}
                  </div>
                </div>
              </div>
            )}

            <div className="mt-4 text-sm text-gray-600">
              <p>💡 Click on any entity to see its connections and relationships</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
