"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Loader2, Youtube, Eye, Globe, FileText, List, Hash, Sparkles } from "lucide-react"

interface SummaryData {
  globalUnderstanding: string
  detailedUnderstanding: string
  stepByStepBreakdown: string[]
  entitiesAndKeywords: string[]
}

export default function Component() {
  const [videoUrl, setVideoUrl] = useState("")
  const [additionalContext, setAdditionalContext] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [summaryData, setSummaryData] = useState<SummaryData | null>(null)
  const [showVisualSummary, setShowVisualSummary] = useState(false)

  const handleSummarize = async () => {
    if (!videoUrl.trim()) return

    setIsLoading(true)

    // Simulate API call
    setTimeout(() => {
      setSummaryData({
        globalUnderstanding:
          "This video provides a comprehensive tutorial on building modern web applications using React and Next.js. The presenter covers fundamental concepts, best practices, and demonstrates how to create a full-stack application with authentication, database integration, and deployment strategies.",
        detailedUnderstanding:
          "The video begins with an introduction to React's component-based architecture and explains the benefits of using Next.js for server-side rendering and static site generation. Key topics include state management with hooks, routing in Next.js, API routes for backend functionality, integration with databases like PostgreSQL, implementing authentication with NextAuth.js, styling with Tailwind CSS, and deployment on Vercel. The presenter also discusses performance optimization techniques, SEO considerations, and modern development workflows.",
        stepByStepBreakdown: [
          "Introduction and project setup with create-next-app",
          "Creating the basic component structure and layout",
          "Setting up routing and navigation between pages",
          "Implementing user authentication with NextAuth.js",
          "Database setup and configuration with Prisma ORM",
          "Building API routes for data fetching and mutations",
          "Styling the application with Tailwind CSS",
          "Adding form validation and error handling",
          "Implementing responsive design patterns",
          "Testing and debugging the application",
          "Deployment configuration and going live on Vercel",
        ],
        entitiesAndKeywords: [
          "React",
          "Next.js",
          "JavaScript",
          "TypeScript",
          "Tailwind CSS",
          "NextAuth.js",
          "Prisma",
          "PostgreSQL",
          "Vercel",
          "API Routes",
          "Server-side Rendering",
          "Static Site Generation",
          "Hooks",
          "Component Architecture",
          "Authentication",
          "Database",
          "Deployment",
        ],
      })
      setIsLoading(false)
    }, 3000)
  }

  const handleReset = () => {
    setVideoUrl("")
    setAdditionalContext("")
    setSummaryData(null)
    setShowVisualSummary(false)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="mx-auto max-w-4xl space-y-6">
        {/* Header */}
        <div className="text-center space-y-2">
          <div className="flex items-center justify-center gap-2">
            <Youtube className="h-8 w-8 text-red-500" />
            <h1 className="text-3xl font-bold text-gray-900">AI Video Summarizer</h1>
          </div>
          <p className="text-gray-600">Transform any YouTube video into comprehensive, structured summaries</p>
        </div>

        {/* Input Section */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Youtube className="h-5 w-5" />
              Video Input
            </CardTitle>
            <CardDescription>Paste the YouTube video URL you want to summarize</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <label htmlFor="video-url" className="text-sm font-medium">
                YouTube Video URL *
              </label>
              <Input
                id="video-url"
                placeholder="https://www.youtube.com/watch?v=..."
                value={videoUrl}
                onChange={(e) => setVideoUrl(e.target.value)}
                disabled={isLoading}
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="additional-context" className="text-sm font-medium">
                Additional Context (Optional)
              </label>
              <Textarea
                id="additional-context"
                placeholder="Provide any additional context or specific aspects you'd like the AI to focus on..."
                value={additionalContext}
                onChange={(e) => setAdditionalContext(e.target.value)}
                disabled={isLoading}
                rows={3}
              />
            </div>

            <div className="flex gap-2">
              <Button onClick={handleSummarize} disabled={!videoUrl.trim() || isLoading} className="flex-1">
                {isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Currently summarizing...
                  </>
                ) : (
                  <>
                    <Sparkles className="mr-2 h-4 w-4" />
                    Summarize Video
                  </>
                )}
              </Button>

              {summaryData && (
                <Button variant="outline" onClick={handleReset}>
                  New Video
                </Button>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Loading State */}
        {isLoading && (
          <Card>
            <CardContent className="flex items-center justify-center py-12">
              <div className="text-center space-y-4">
                <Loader2 className="h-12 w-12 animate-spin mx-auto text-blue-500" />
                <div className="space-y-2">
                  <h3 className="text-lg font-semibold">Processing your video...</h3>
                  <p className="text-gray-600">
                    Our AI is analyzing the content and generating comprehensive summaries
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Summary Results */}
        {summaryData && !isLoading && (
          <div className="space-y-6">
            {/* Visual Summary Button */}
            <div className="flex justify-center">
              <Button variant="outline" onClick={() => setShowVisualSummary(!showVisualSummary)} className="bg-white">
                <Eye className="mr-2 h-4 w-4" />
                {showVisualSummary ? "Hide" : "Show"} Visual Summary
              </Button>
            </div>

            {/* Visual Summary */}
            {showVisualSummary && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Eye className="h-5 w-5" />
                    Visual Summary
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="bg-gray-50 rounded-lg p-8 text-center">
                    <div className="space-y-4">
                      <div className="text-4xl">🎥</div>
                      <div className="text-lg font-semibold">Video Content Flow</div>
                      <div className="flex items-center justify-center gap-4 text-sm">
                        <div className="bg-blue-100 px-3 py-1 rounded">Setup</div>
                        <div>→</div>
                        <div className="bg-green-100 px-3 py-1 rounded">Implementation</div>
                        <div>→</div>
                        <div className="bg-purple-100 px-3 py-1 rounded">Deployment</div>
                      </div>
                      <p className="text-gray-600 text-sm">
                        Interactive visual diagrams and flowcharts would be generated here
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Global Understanding */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Globe className="h-5 w-5 text-blue-500" />
                  Global Understanding
                </CardTitle>
                <CardDescription>High-level overview of the video content</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-gray-700 leading-relaxed">{summaryData.globalUnderstanding}</p>
              </CardContent>
            </Card>

            {/* Detailed Understanding */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="h-5 w-5 text-green-500" />
                  Detailed Understanding
                </CardTitle>
                <CardDescription>In-depth analysis of key concepts and ideas</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-gray-700 leading-relaxed">{summaryData.detailedUnderstanding}</p>
              </CardContent>
            </Card>

            {/* Step-by-Step Breakdown */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <List className="h-5 w-5 text-purple-500" />
                  Step-by-Step Breakdown
                </CardTitle>
                <CardDescription>Chronological or instructional summary</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {summaryData.stepByStepBreakdown.map((step, index) => (
                    <div key={index} className="flex gap-3">
                      <div className="flex-shrink-0 w-6 h-6 bg-purple-100 text-purple-600 rounded-full flex items-center justify-center text-sm font-semibold">
                        {index + 1}
                      </div>
                      <p className="text-gray-700 pt-0.5">{step}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Entities and Keywords */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Hash className="h-5 w-5 text-orange-500" />
                  Entities and Keywords
                </CardTitle>
                <CardDescription>Key people, concepts, and terms mentioned</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {summaryData.entitiesAndKeywords.map((keyword, index) => (
                    <Badge key={index} variant="secondary" className="bg-orange-50 text-orange-700 hover:bg-orange-100">
                      {keyword}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  )
}
