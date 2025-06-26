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
  const [selectedKeyword, setSelectedKeyword] = useState<string | null>(null)
  const [keywordDefinitions] = useState<Record<string, string>>({
    React:
      "A JavaScript library for building user interfaces, particularly web applications, using a component-based architecture.",
    "Next.js":
      "A React framework that provides features like server-side rendering, static site generation, and API routes for building full-stack web applications.",
    JavaScript:
      "A high-level, interpreted programming language that is one of the core technologies of the World Wide Web, alongside HTML and CSS.",
    TypeScript:
      "A strongly typed programming language that builds on JavaScript by adding static type definitions, developed by Microsoft.",
    "Tailwind CSS":
      "A utility-first CSS framework that provides low-level utility classes to build custom designs without writing custom CSS.",
    "NextAuth.js":
      "A complete open-source authentication solution for Next.js applications, supporting multiple providers and authentication methods.",
    Prisma:
      "A next-generation ORM (Object-Relational Mapping) tool that provides type-safe database access and automatic migrations.",
    PostgreSQL:
      "A powerful, open-source object-relational database system known for its reliability, feature robustness, and performance.",
    Vercel:
      "A cloud platform for static sites and serverless functions that provides deployment and hosting services, particularly optimized for Next.js.",
    "API Routes":
      "Server-side functions in Next.js that allow you to build API endpoints within your Next.js application.",
    "Server-side Rendering":
      "A technique where web pages are rendered on the server before being sent to the client, improving initial load times and SEO.",
    "Static Site Generation":
      "A method of pre-building web pages at build time, resulting in fast-loading static HTML files.",
    Hooks: "Functions in React that let you use state and other React features in functional components.",
    "Component Architecture":
      "A design pattern that breaks down the user interface into reusable, independent components.",
    Authentication: "The process of verifying the identity of users before granting access to protected resources.",
    Database:
      "An organized collection of structured information or data, typically stored electronically in a computer system.",
    Deployment: "The process of making a software application available for use in a production environment.",
  })

const handleSummarize = async () => {
  if (!videoUrl.trim()) return;

  setIsLoading(true);

  try {
   const response = await fetch("http://localhost:8000/summarize", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    vid_url: videoUrl
  })
});
const data = await response.json();
setSummaryData({
        globalUnderstanding:data['Goal'],
        detailedUnderstanding: data['Global Understanding'],
        stepByStepBreakdown:[data['Steps']],
        entitiesAndKeywords:["data['Entities']","just","workd"]
          })

console.log(data);
  } catch (error) {
    console.error("Error summarizing video:", error);
    // Optionally handle error UI
  } finally {
    setIsLoading(false);
  }
}


  const handleReset = () => {
    setVideoUrl("")
    setAdditionalContext("")
    setSummaryData(null)
    setShowVisualSummary(false)
  }

  const handleKeywordClick = (keyword: string) => {
    setSelectedKeyword(selectedKeyword === keyword ? null : keyword)
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
                <CardDescription>Key people, concepts, and terms mentioned (click for definitions)</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex flex-wrap gap-2">
                  {summaryData.entitiesAndKeywords.map((keyword, index) => (
                    <Badge
                      key={index}
                      variant="secondary"
                      className={`cursor-pointer transition-colors ${
                        selectedKeyword === keyword
                          ? "bg-orange-200 text-orange-800 hover:bg-orange-300"
                          : "bg-orange-50 text-orange-700 hover:bg-orange-100"
                      }`}
                      onClick={() => handleKeywordClick(keyword)}
                    >
                      {keyword}
                    </Badge>
                  ))}
                </div>

                {/* Definition Display */}
                {selectedKeyword && keywordDefinitions[selectedKeyword] && (
                  <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                    <div className="flex items-start gap-2">
                      <div className="flex-shrink-0 w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-bold">
                        i
                      </div>
                      <div className="space-y-1">
                        <h4 className="font-semibold text-blue-900">{selectedKeyword}</h4>
                        <p className="text-blue-800 text-sm leading-relaxed">{keywordDefinitions[selectedKeyword]}</p>
                      </div>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  )
}
