import { RelationshipGraph } from "./relationship-graph"


type Triple = [string, string, string];

type GComponentProps = {
  data?: Triple[];
};

export default function GComponent({ data }: GComponentProps) {
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
  const effectiveData = data?.length ? data : sampleData;

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
            <RelationshipGraph  data={effectiveData} width={600} height={400} className="mx-auto" />
          </div>
        </div>

   
      </div>
    </div>
  )
}
