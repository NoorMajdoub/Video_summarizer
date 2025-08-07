"use client"

import type React from "react"
import GComponent from "./graph-structure"

import { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Checkbox } from "@/components/ui/checkbox"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
  Loader2,
  Youtube,
  Eye,
  Globe,
  FileText,
  List,
  Hash,
  Sparkles,
  UserIcon,
  LogOut,
  Settings,
  Code,
  Copy,
  Check,
} from "lucide-react"

interface SummaryData {
  globalUnderstanding: string
  detailedUnderstanding: string
  stepByStepBreakdown: string[]
  entitiesAndKeywords: string[]
  extractedCode?: CodeBlock[]
}

interface CodeBlock {
  language: string
  title: string
  code: string
  description: string
}

interface UserData {
  name: string
  email: string
  avatar?: string
}

interface VideoHistory {
  id: string
  title: string
  url: string
  thumbnail: string
  date: string
  summary: SummaryData
}

export default function Component() {
  const [videoUrl, setVideoUrl] = useState("")
  const [additionalContext, setAdditionalContext] = useState("")
  const [extractCode, setExtractCode] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [summaryData, setSummaryData] = useState<SummaryData | null>(null)
  const [showVisualSummary, setShowVisualSummary] = useState(false)
  const [selectedKeyword, setSelectedKeyword] = useState<string | null>(null)
  const [user, setUser] = useState<UserData | null>(null)
  const [showLogin, setShowLogin] = useState(false)
  const [loginForm, setLoginForm] = useState({ email: "", password: "" })
  const [copiedCode, setCopiedCode] = useState<string | null>(null)

  //the visual
  type Triple = [string, string, string];
  const [visdata, setvisData] = useState<Triple[]>();

  const [videoHistory, setVideoHistory] = useState<VideoHistory[]>([
    // Mock data for demonstration
    {
      id: "1",
      title: "React Hooks Tutorial - Complete Guide",
      url: "https://www.youtube.com/watch?v=example1",
      thumbnail: "/placeholder.svg?height=90&width=160",
      date: "2024-01-15",
      summary: {
        globalUnderstanding:
          "Comprehensive tutorial covering React Hooks including useState, useEffect, and custom hooks.",
        detailedUnderstanding: "The video explains the motivation behind hooks, their rules, and practical examples.",
        stepByStepBreakdown: ["Introduction to Hooks", "useState Hook", "useEffect Hook", "Custom Hooks"],
        entitiesAndKeywords: ["React", "Hooks", "useState", "useEffect"],
      },
    },
    {
      id: "2",
      title: "Next.js 14 App Router Deep Dive",
      url: "https://www.youtube.com/watch?v=example2",
      thumbnail: "/placeholder.svg?height=90&width=160",
      date: "2024-01-10",
      summary: {
        globalUnderstanding: "Deep dive into Next.js 14 App Router architecture and new features.",
        detailedUnderstanding: "Covers server components, streaming, and the new file-based routing system.",
        stepByStepBreakdown: ["App Router Setup", "Server Components", "Client Components", "Streaming"],
        entitiesAndKeywords: ["Next.js", "App Router", "Server Components", "Streaming"],
      },
    },
  ])
  const [selectedHistoryItem, setSelectedHistoryItem] = useState<VideoHistory | null>(null)

const [keywordDefinitions, setKeywordDefinitions] = useState<Record<string, string>>({});
const getcode = () => {
  console.log("Button clicked!");
  // Add your code logic here
};

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault()
    // Simulate login
    setUser({
      name: "John Doe",
      email: loginForm.email,
      avatar: "/placeholder.svg?height=32&width=32",
    })
    setShowLogin(false)
    setLoginForm({ email: "", password: "" })
  }

  const handleLogout = () => {
    setUser(null)
    setSummaryData(null)
    setVideoUrl("")
    setAdditionalContext("")
    setExtractCode(false)
  }

const handleSummarize = async () => {
  if (!videoUrl.trim()) return;

  setIsLoading(true);
console.log("hi")
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
console.log("dataaaa3")
console.log(data["visual"])
setvisData(data["visual"])
     if (extractCode) {
        setSummaryData({
         globalUnderstanding:data['goal'],
        detailedUnderstanding: data['global_understanding'],
        stepByStepBreakdown:data["steps"],
        entitiesAndKeywords:data['entities'],
          // not yet used 
          extractedCode: [
            {
              language: "javascript",
              title: "React Component Setup",
              code: `import React, { useState } from 'react'`,
              description: "Basic React login form component with state management using hooks",
            }
          ],
       
        })
      } else {

setSummaryData({
        globalUnderstanding:data['goal'],
        detailedUnderstanding: data['global_understanding'],
        stepByStepBreakdown:data["steps"],
        entitiesAndKeywords:data.entities.map(([key, value]: [string, string]) => [key.trim()])
          })
if (data?.entities) {
    const entries = Object.fromEntries(
      data.entities.map(([key, value]: [string, string]) => [key.trim(), value.trim()])
    );
    setKeywordDefinitions(entries);
  }
console.log(data);
 }
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
    setExtractCode(false)
    setSelectedHistoryItem(null)
  }

  const handleKeywordClick = (keyword: string) => {
    setSelectedKeyword(selectedKeyword === keyword ? null : keyword)
  }

  const copyToClipboard = async (code: string, title: string) => {
    try {
      await navigator.clipboard.writeText(code)
      setCopiedCode(title)
      setTimeout(() => setCopiedCode(null), 2000)
    } catch (err) {
      console.error("Failed to copy code:", err)
    }
  }

  const viewHistoryItem = (item: VideoHistory) => {
    setSelectedHistoryItem(item)
    setSummaryData(item.summary)
    setVideoUrl(item.url)
    setShowVisualSummary(false)
  }

  const deleteHistoryItem = (id: string) => {
    setVideoHistory((prev) => prev.filter((item) => item.id !== id))
    if (selectedHistoryItem?.id === id) {
      setSelectedHistoryItem(null)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="mx-auto max-w-4xl space-y-6">
        {/* Header with Login */}
        <div className="flex items-center justify-between">
          <div className="text-center space-y-2 flex-1">
            <div className="flex items-center justify-center gap-2">
              <Youtube className="h-8 w-8 text-red-500" />
              <h1 className="text-3xl font-bold text-gray-900">AI Video Summarizer</h1>
            </div>
            <p className="text-gray-600">Transform any YouTube video into comprehensive, structured summaries</p>
          </div>

          {/* User Menu */}
          <div className="flex items-center gap-4">
            {user ? (
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" className="relative h-10 w-10 rounded-full">
                    <Avatar className="h-10 w-10">
                      <AvatarImage src={user.avatar || "/placeholder.svg"} alt={user.name} />
                      <AvatarFallback>
                        {user.name
                          .split(" ")
                          .map((n) => n[0])
                          .join("")}
                      </AvatarFallback>
                    </Avatar>
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent className="w-56" align="end">
                  <div className="flex items-center justify-start gap-2 p-2">
                    <div className="flex flex-col space-y-1 leading-none">
                      <p className="font-medium">{user.name}</p>
                      <p className="w-[200px] truncate text-sm text-muted-foreground">{user.email}</p>
                    </div>
                  </div>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem>
                    <Settings className="mr-2 h-4 w-4" />
                    Settings
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={handleLogout}>
                    <LogOut className="mr-2 h-4 w-4" />
                    Log out
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            ) : (
              <Button onClick={() => setShowLogin(true)} variant="outline">
                <UserIcon className="mr-2 h-4 w-4" />
                Login
              </Button>
            )}
          </div>
        </div>

        {/* Login Modal */}
        {showLogin && !user && (
          <Card className="max-w-md mx-auto">
            <CardHeader>
              <CardTitle>Login to Your Account</CardTitle>
              <CardDescription>Access your saved summaries and preferences</CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleLogin} className="space-y-4">
                <div className="space-y-2">
                  <label htmlFor="login-email" className="text-sm font-medium">
                    Email
                  </label>
                  <Input
                    id="login-email"
                    type="email"
                    placeholder="Enter your email"
                    value={loginForm.email}
                    onChange={(e) => setLoginForm((prev) => ({ ...prev, email: e.target.value }))}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <label htmlFor="login-password" className="text-sm font-medium">
                    Password
                  </label>
                  <Input
                    id="login-password"
                    type="password"
                    placeholder="Enter your password"
                    value={loginForm.password}
                    onChange={(e) => setLoginForm((prev) => ({ ...prev, password: e.target.value }))}
                    required
                  />
                </div>
                <div className="flex gap-2">
                  <Button type="submit" className="flex-1">
                    Login
                  </Button>
                  <Button type="button" variant="outline" onClick={() => setShowLogin(false)}>
                    Cancel
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        )}

        {/* Input Section */}
        {(!showLogin || user) && (
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

              {/* Code Extraction Option */}
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="extract-code"
                  checked={extractCode}
                  onCheckedChange={(checked) => setExtractCode(checked as boolean)}
                  disabled={isLoading}
                />
                <label
                  htmlFor="extract-code"
                  className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                >
                      <Button
          
            onClick={getcode}
            className="flex-1"
          >
            Getcode
            </Button>
                </label>
              </div>

              <div className="flex gap-2">
                <Button
                  onClick={handleSummarize}
                  disabled={!videoUrl.trim() || isLoading || (extractCode && !user)}
                  className="flex-1"
                >
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
        )}

        {/* Video History Section - Only show when logged in */}
        {user && videoHistory.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="h-5 w-5 text-indigo-500" />
                Your Video History
              </CardTitle>
              <CardDescription>Previously summarized videos</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {videoHistory.map((item) => (
                  <div
                    key={item.id}
                    className={`flex items-center gap-4 p-3 rounded-lg border transition-colors cursor-pointer ${
                      selectedHistoryItem?.id === item.id
                        ? "bg-indigo-50 border-indigo-200"
                        : "bg-gray-50 hover:bg-gray-100 border-gray-200"
                    }`}
                    onClick={() => viewHistoryItem(item)}
                  >
                    <img
                      src={item.thumbnail || "/placeholder.svg"}
                      alt="Video thumbnail"
                      className="w-20 h-12 object-cover rounded"
                    />
                    <div className="flex-1 min-w-0">
                      <h4 className="font-medium text-gray-900 truncate">{item.title}</h4>
                      <p className="text-sm text-gray-500 truncate">{item.url}</p>
                      <p className="text-xs text-gray-400">
                        {new Date(item.date).toLocaleDateString("en-US", {
                          year: "numeric",
                          month: "short",
                          day: "numeric",
                        })}
                      </p>
                    </div>
                    <div className="flex items-center gap-2">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation()
                          viewHistoryItem(item)
                        }}
                      >
                        View
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation()
                          deleteHistoryItem(item.id)
                        }}
                        className="text-red-600 hover:text-red-700 hover:bg-red-50"
                      >
                        Delete
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

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
                    {extractCode && " with code extraction"}
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
               <GComponent  data={visdata}/>
              </Card>
            )}

            {/* Extracted Code Section */}
            {summaryData.extractedCode && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Code className="h-5 w-5 text-green-500" />
                    Extracted Code
                  </CardTitle>
                  <CardDescription>Code snippets and examples from the video</CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  {summaryData.extractedCode.map((codeBlock, index) => (
                    <div key={index} className="space-y-3">
                      <div className="flex items-center justify-between">
                        <div>
                          <h4 className="font-semibold text-gray-900">{codeBlock.title}</h4>
                          <p className="text-sm text-gray-600">{codeBlock.description}</p>
                        </div>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => copyToClipboard(codeBlock.code, codeBlock.title)}
                          className="flex items-center gap-2"
                        >
                          {copiedCode === codeBlock.title ? (
                            <>
                              <Check className="h-4 w-4" />
                              Copied
                            </>
                          ) : (
                            <>
                              <Copy className="h-4 w-4" />
                              Copy
                            </>
                          )}
                        </Button>
                      </div>
                      <div className="bg-gray-900 rounded-lg p-4 overflow-x-auto">
                        <pre className="text-sm text-gray-100">
                          <code>{codeBlock.code}</code>
                        </pre>
                      </div>
                    </div>
                  ))}
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
