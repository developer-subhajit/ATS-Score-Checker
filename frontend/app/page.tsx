"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Upload, FileText, ClipboardPaste, ArrowRight } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import {
  Alert,
  AlertDescription,
  AlertTitle,
} from "@/components/ui/alert";
import { useToast } from "@/hooks/use-toast";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";

export default function Home() {
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [resumeText, setResumeText] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [activeTab, setActiveTab] = useState<"upload" | "paste">("upload");
  const [jdActiveTab, setJdActiveTab] = useState<"paste" | "upload">("paste");
  const { toast } = useToast();

  const handleFileDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    validateAndSetFile(droppedFile);
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const validateAndSetFile = (file: File) => {
    const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    if (!validTypes.includes(file.type)) {
      toast({
        title: "Invalid file format",
        description: "Please upload a PDF or DOCX file",
        variant: "destructive",
      });
      return;
    }
    setFile(file);
    toast({
      title: "File uploaded successfully",
      description: `${file.name} has been uploaded`,
    });
  };

  const handleJDFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const text = e.target?.result;
        if (typeof text === 'string') {
          setJobDescription(text);
          toast({
            title: "Job Description loaded",
            description: "File contents have been loaded successfully",
          });
        }
      };
      reader.readAsText(e.target.files[0]);
    }
  };

  const analyzeResume = async () => {
    if ((!file && !resumeText) || !jobDescription) {
      toast({
        title: "Missing information",
        description: "Please provide both a resume and job description",
        variant: "destructive",
      });
      return;
    }

    setIsAnalyzing(true);
    
    // Simulated analysis - replace with actual API call
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    const results = {
      overallScore: 85,
      keywordMatch: 78,
      missingKeywords: ["Docker", "Kubernetes", "CI/CD"],
      formatScore: 92,
      improvements: [
        "Add more quantifiable achievements",
        "Include Docker experience",
        "Expand on leadership roles"
      ]
    };
    
    setIsAnalyzing(false);
    
    // Store results in localStorage for the results page
    localStorage.setItem('atsResults', JSON.stringify(results));
    router.push('/results');
  };

  return (
    <main className="min-h-screen bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-blue-100 via-blue-50 to-white dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-4 animate-fade-in">
            ATS Resume Checker
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Optimize your resume for Applicant Tracking Systems and increase your chances of landing an interview
          </p>
        </div>

        <div className="grid gap-8 md:grid-cols-2">
          {/* Resume Section */}
          <Card className="p-6 backdrop-blur-sm bg-white/50 dark:bg-gray-900/50 border-2 hover:border-blue-500 transition-all duration-300">
            <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <FileText className="h-5 w-5 text-blue-500" />
              Resume
            </h3>
            
            <div className="flex gap-2 mb-4">
              <Button
                variant={activeTab === "upload" ? "default" : "outline"}
                onClick={() => setActiveTab("upload")}
                className="flex-1"
              >
                <Upload className="h-4 w-4 mr-2" />
                Upload
              </Button>
              <Button
                variant={activeTab === "paste" ? "default" : "outline"}
                onClick={() => setActiveTab("paste")}
                className="flex-1"
              >
                <ClipboardPaste className="h-4 w-4 mr-2" />
                Paste
              </Button>
            </div>

            <div className="h-[400px] overflow-y-auto">
              {activeTab === "upload" ? (
                <div
                  onDragOver={(e) => e.preventDefault()}
                  onDrop={handleFileDrop}
                  className="h-full border-2 border-dashed rounded-lg p-8 text-center hover:border-blue-500 cursor-pointer transition-all duration-300 bg-white/50 dark:bg-gray-800/50 flex flex-col items-center justify-center"
                >
                  <input
                    type="file"
                    id="resume-upload"
                    accept=".pdf,.docx"
                    onChange={handleFileInput}
                    className="hidden"
                  />
                  <label htmlFor="resume-upload" className="cursor-pointer">
                    <Upload className="mx-auto h-12 w-12 text-blue-500 mb-4" />
                    <h3 className="text-lg font-semibold mb-2">
                      Upload your resume
                    </h3>
                    <p className="text-sm text-gray-500 mb-2">
                      Drop your PDF or DOCX file here, or click to browse
                    </p>
                    {file && (
                      <Alert className="mt-4">
                        <FileText className="h-4 w-4" />
                        <AlertTitle>File uploaded</AlertTitle>
                        <AlertDescription>{file.name}</AlertDescription>
                      </Alert>
                    )}
                  </label>
                </div>
              ) : (
                <Textarea
                  placeholder="Paste your resume text here..."
                  className="h-full resize-none bg-white/50 dark:bg-gray-800/50"
                  value={resumeText}
                  onChange={(e) => setResumeText(e.target.value)}
                />
              )}
            </div>
          </Card>

          {/* Job Description Section */}
          <Card className="p-6 backdrop-blur-sm bg-white/50 dark:bg-gray-900/50 border-2 hover:border-purple-500 transition-all duration-300">
            <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <FileText className="h-5 w-5 text-purple-500" />
              Job Description
            </h3>

            <div className="flex gap-2 mb-4">
              <Button
                variant={jdActiveTab === "paste" ? "default" : "outline"}
                onClick={() => setJdActiveTab("paste")}
                className="flex-1"
              >
                <ClipboardPaste className="h-4 w-4 mr-2" />
                Paste
              </Button>
              <Button
                variant={jdActiveTab === "upload" ? "default" : "outline"}
                onClick={() => setJdActiveTab("upload")}
                className="flex-1"
              >
                <Upload className="h-4 w-4 mr-2" />
                Upload
              </Button>
            </div>

            <div className="h-[400px] overflow-y-auto">
              {jdActiveTab === "paste" ? (
                <Textarea
                  placeholder="Paste the job description here..."
                  className="h-full resize-none bg-white/50 dark:bg-gray-800/50"
                  value={jobDescription}
                  onChange={(e) => setJobDescription(e.target.value)}
                />
              ) : (
                <div
                  className="h-full border-2 border-dashed rounded-lg p-8 text-center hover:border-purple-500 cursor-pointer transition-all duration-300 bg-white/50 dark:bg-gray-800/50 flex flex-col items-center justify-center"
                >
                  <input
                    type="file"
                    id="jd-upload"
                    accept=".txt,.pdf,.docx"
                    onChange={handleJDFileInput}
                    className="hidden"
                  />
                  <label htmlFor="jd-upload" className="cursor-pointer">
                    <Upload className="mx-auto h-12 w-12 text-purple-500 mb-4" />
                    <h3 className="text-lg font-semibold mb-2">
                      Upload job description
                    </h3>
                    <p className="text-sm text-gray-500 mb-2">
                      Upload a TXT, PDF, or DOCX file
                    </p>
                  </label>
                </div>
              )}
            </div>
          </Card>
        </div>

        <div className="mt-8 text-center">
          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger asChild>
                <span>
                  <Button
                    size="lg"
                    onClick={analyzeResume}
                    disabled={isAnalyzing || (!file && !resumeText) || !jobDescription}
                    className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-8 py-6 text-lg"
                  >
                    {isAnalyzing ? (
                      "Analyzing..."
                    ) : (
                      <>
                        Analyze Resume
                        <ArrowRight className="ml-2 h-5 w-5" />
                      </>
                    )}
                  </Button>
                </span>
              </TooltipTrigger>
              <TooltipContent>
                {(!file && !resumeText) || !jobDescription
                  ? "Please provide both resume and job description"
                  : "Click to analyze your resume"}
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>
        </div>
      </div>
    </main>
  );
}