import { RelationshipGraph } from "./relationship-graph"
export default function GComponent() {
  // Example data showing various entity relationships
  const sampleData: [string, string, string][] = [
    ["User", "creates", "Post"],
    ["Post", "belongs to", "Category"],
    ["User", "follows", "User"],
    ["Comment", "replies to", "Post"],
    ["User", "writes", "Comment"],
    ["Category", "contains", "Post"],
    ["Post", "has", "Tag"],
    ["Tag", "categorizes", "Post"],
  ]

  const simpleData: [string, string, string][] = [
    ["Alice", "knows", "Bob"],
    ["Bob", "works with", "Charlie"],
    ["Charlie", "mentors", "Alice"],
    ["Alice", "collaborates", "David"],
  ]

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto space-y-8">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Relationship Graph Visualizer</h1>
          <p className="text-gray-600">Visual representation of entities and their relationships</p>
        </div>

        <div className="space-y-8">
          <div>
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Social Network Example</h2>
            <RelationshipGraph data={simpleData} width={600} height={400} className="mx-auto" />
          </div>

          <div>
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Content Management System</h2>
            <RelationshipGraph data={sampleData} width={800} height={600} className="mx-auto" />
          </div>
        </div>

        <div className="bg-white rounded-lg p-6 border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-800 mb-3">Usage Example</h3>
          <pre className="bg-gray-100 p-4 rounded text-sm overflow-x-auto">
            {`const data = [
  ["Entity1", "Relation", "Entity2"],
  ["Entity3", "Relation", "Entity4"],
  // ... more relationships
]

<RelationshipGraph 
  data={data} 
  width={800} 
  height={600} 
/>`}
          </pre>
        </div>
      </div>
    </div>
  )
}
