"use client"

import { useMemo } from "react"

interface RelationshipGraphProps {
  data: [string, string, string][]
  width?: number
  height?: number
  className?: string
}

interface Node {
  id: string
  x: number
  y: number
}

interface Edge {
  source: string
  target: string
  label: string
}

export function RelationshipGraph({ data, width = 800, height = 600, className = "" }: RelationshipGraphProps) {
  const { nodes, edges } = useMemo(() => {
    // Extract unique entities
    const entitySet = new Set<string>()
    const edgeList: Edge[] = []

    data.forEach(([source, relation, target]) => {
      entitySet.add(source)
      entitySet.add(target)
      edgeList.push({ source, target, label: relation })
    })

    const entities = Array.from(entitySet)
    const nodeCount = entities.length

    // Position nodes in a circle
    const centerX = width / 2
    const centerY = height / 2
    const radius = Math.min(width, height) * 0.3

    const nodeList: Node[] = entities.map((entity, index) => {
      const angle = (2 * Math.PI * index) / nodeCount
      return {
        id: entity,
        x: centerX + radius * Math.cos(angle),
        y: centerY + radius * Math.sin(angle),
      }
    })

    return { nodes: nodeList, edges: edgeList }
  }, [data, width, height])

  const getNodeById = (id: string) => nodes.find((node) => node.id === id)

  const createArrowPath = (x1: number, y1: number, x2: number, y2: number, nodeRadius = 30) => {
    // Calculate direction vector
    const dx = x2 - x1
    const dy = y2 - y1
    const length = Math.sqrt(dx * dx + dy * dy)

    // Normalize direction
    const unitX = dx / length
    const unitY = dy / length

    // Adjust start and end points to account for node radius
    const startX = x1 + unitX * nodeRadius
    const startY = y1 + unitY * nodeRadius
    const endX = x2 - unitX * nodeRadius
    const endY = y2 - unitY * nodeRadius

    return { startX, startY, endX, endY, unitX, unitY }
  }

  return (
    <div className={`bg-white border border-gray-200 rounded-lg p-4 ${className}`}>
      <svg width={width} height={height} className="overflow-visible">
        {/* Define arrow marker */}
        <defs>
          <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
            <polygon points="0 0, 10 3.5, 0 7" fill="#374151" />
          </marker>
        </defs>

        {/* Draw edges */}
        {edges.map((edge, index) => {
          const sourceNode = getNodeById(edge.source)
          const targetNode = getNodeById(edge.target)

          if (!sourceNode || !targetNode) return null

          const { startX, startY, endX, endY } = createArrowPath(sourceNode.x, sourceNode.y, targetNode.x, targetNode.y)

          // Calculate label position (midpoint of the edge)
          const labelX = (startX + endX) / 2
          const labelY = (startY + endY) / 2

          return (
            <g key={`edge-${index}`}>
              {/* Edge line */}
              <line
                x1={startX}
                y1={startY}
                x2={endX}
                y2={endY}
                stroke="#374151"
                strokeWidth="2"
                markerEnd="url(#arrowhead)"
              />

              {/* Edge label */}
              <rect
                x={labelX - edge.label.length * 4}
                y={labelY - 10}
                width={edge.label.length * 8}
                height={20}
                fill="white"
                stroke="#e5e7eb"
                strokeWidth="1"
                rx="4"
              />
              <text x={labelX} y={labelY + 4} textAnchor="middle" className="text-xs font-medium fill-gray-700">
                {edge.label}
              </text>
            </g>
          )
        })}

        {/* Draw nodes */}
        {nodes.map((node) => (
          <g key={node.id}>
            {/* Node circle */}
            <circle cx={node.x} cy={node.y} r="30" fill="#f3f4f6" stroke="#374151" strokeWidth="2" />

            {/* Node label */}
            <text
              x={node.x}
              y={node.y + 4}
              textAnchor="middle"
              className="text-sm font-semibold fill-gray-800 pointer-events-none"
            >
              {node.id}
            </text>
          </g>
        ))}
      </svg>
    </div>
  )
}
