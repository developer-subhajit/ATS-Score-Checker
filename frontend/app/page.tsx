"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import {
    Upload,
    FileText,
    ClipboardPaste,
    ArrowRight,
    Trophy,
    Loader2,
    Sparkles,
} from "lucide-react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { useToast } from "@/hooks/use-toast";
import {
    Tooltip,
    TooltipContent,
    TooltipProvider,
    TooltipTrigger,
} from "@/components/ui/tooltip";
import { uploadResume, uploadJobDescription, calculateScore } from "@/lib/api";

export default function Home() {
    const router = useRouter();
    const [resumeFile, setResumeFile] = useState<File | null>(null);
    const [resumeText, setResumeText] = useState("");
    const [resumeActiveTab, setResumeActiveTab] = useState<"upload" | "paste">(
        "upload"
    );

    const [jobFile, setJobFile] = useState<File | null>(null);
    const [jobText, setJobText] = useState("");
    const [jobActiveTab, setJobActiveTab] = useState<"upload" | "paste">(
        "upload"
    );

    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const { toast } = useToast();

    const handleFileDrop = (e: React.DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        const droppedFile = e.dataTransfer.files[0];
        validateAndSetFile(droppedFile, "resume");
    };

    const handleFileInput = (
        e: React.ChangeEvent<HTMLInputElement>,
        type: "resume" | "job"
    ) => {
        const file = e.target.files?.[0] || null;
        validateAndSetFile(file, type);
    };

    const validateAndSetFile = (file: File | null, type: "resume" | "job") => {
        if (!file) {
            toast({
                title: "Error",
                description: "No file selected",
                variant: "destructive",
            });
            return;
        }

        // Check file type
        const validTypes = [
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "text/plain",
        ];

        if (!validTypes.includes(file.type)) {
            toast({
                title: "Invalid file type",
                description: "Please upload a PDF, DOCX, or TXT file",
                variant: "destructive",
            });
            return;
        }

        // Check file size (10MB limit)
        const maxSize = 10 * 1024 * 1024; // 10MB
        if (file.size > maxSize) {
            toast({
                title: "File too large",
                description: "Please upload a file smaller than 10MB",
                variant: "destructive",
            });
            return;
        }

        // Set the appropriate file state
        if (type === "resume") {
            setResumeFile(file);
            setResumeText("");
            toast({
                title: "Resume uploaded",
                description: "Resume file has been loaded successfully",
            });
        } else {
            setJobFile(file);
            setJobText("");
            toast({
                title: "Job Description uploaded",
                description:
                    "Job Description file has been loaded successfully",
            });
        }
    };

    const handlePaste = (
        e: React.ClipboardEvent<HTMLTextAreaElement>,
        type: "resume" | "job"
    ) => {
        const text = e.clipboardData.getData("text");
        if (text) {
            if (type === "resume") {
                setResumeText(text);
                setResumeFile(null);
                toast({
                    title: "Resume pasted",
                    description: "Resume text has been loaded successfully",
                });
            } else {
                setJobText(text);
                setJobFile(null);
                toast({
                    title: "Job Description pasted",
                    description:
                        "Job Description text has been loaded successfully",
                });
            }
        }
    };

    const handleDrop = async (
        e: React.DragEvent<HTMLDivElement>,
        type: "resume" | "job"
    ) => {
        e.preventDefault();
        const file = e.dataTransfer.files?.[0] || null;
        validateAndSetFile(file, type);
    };

    const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        e.currentTarget.classList.add("border-blue-500");
    };

    const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        e.currentTarget.classList.remove("border-blue-500");
    };

    const analyzeResume = async () => {
        try {
            setIsAnalyzing(true);

            // Upload resume
            let resumeId;
            try {
                if (resumeFile) {
                    const resumeResponse = await uploadResume(resumeFile);
                    resumeId = resumeResponse.file_id;
                } else if (resumeText) {
                    const resumeBlob = new Blob([resumeText], {
                        type: "text/plain",
                    });
                    const resumeTextFile = new File(
                        [resumeBlob],
                        "resume.txt",
                        { type: "text/plain" }
                    );
                    const resumeResponse = await uploadResume(resumeTextFile);
                    resumeId = resumeResponse.file_id;
                } else {
                    throw new Error("No resume content provided");
                }
            } catch (error) {
                toast({
                    title: "Resume upload failed",
                    description: error.message || "Failed to upload resume",
                    variant: "destructive",
                });
                return;
            }

            // Upload job description
            let jobId;
            try {
                if (jobFile) {
                    const jobResponse = await uploadJobDescription(jobFile);
                    jobId = jobResponse.file_id;
                } else if (jobText) {
                    const jobResponse = await uploadJobDescription(jobText);
                    jobId = jobResponse.file_id;
                } else {
                    throw new Error("No job description content provided");
                }
            } catch (error) {
                toast({
                    title: "Job description upload failed",
                    description:
                        error.message || "Failed to upload job description",
                    variant: "destructive",
                });
                return;
            }

            // Calculate scores
            try {
                const scores = await calculateScore(resumeId, jobId);
                localStorage.setItem("atsResults", JSON.stringify(scores));
                router.push("/results");
            } catch (error) {
                toast({
                    title: "Analysis failed",
                    description: error.message || "Failed to analyze resume",
                    variant: "destructive",
                });
            }
        } finally {
            setIsAnalyzing(false);
        }
    };

    return (
        <main className="min-h-screen bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-blue-100 via-blue-50 to-white dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-5xl mx-auto">
                <div className="text-center mb-12">
                    <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-4 animate-fade-in">
                        ATS Resume Checker
                    </h1>
                    <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto mb-4">
                        Optimize your resume for Applicant Tracking Systems and
                        increase your chances of landing an interview
                    </p>
                    <Button
                        variant="outline"
                        onClick={() => router.push("/rankings")}
                        className="gap-2"
                    >
                        <Trophy className="h-4 w-4" />
                        View Rankings
                    </Button>
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
                                variant={
                                    resumeActiveTab === "upload"
                                        ? "default"
                                        : "outline"
                                }
                                onClick={() => setResumeActiveTab("upload")}
                                className="flex-1"
                            >
                                <Upload className="h-4 w-4 mr-2" />
                                Upload
                            </Button>
                            <Button
                                variant={
                                    resumeActiveTab === "paste"
                                        ? "default"
                                        : "outline"
                                }
                                onClick={() => setResumeActiveTab("paste")}
                                className="flex-1"
                            >
                                <ClipboardPaste className="h-4 w-4 mr-2" />
                                Paste
                            </Button>
                        </div>

                        <div
                            onDragOver={handleDragOver}
                            onDragLeave={handleDragLeave}
                            onDrop={(e) => handleDrop(e, "resume")}
                            className="h-[400px] overflow-y-auto"
                        >
                            {resumeActiveTab === "upload" ? (
                                <div className="h-full border-2 border-dashed rounded-lg p-8 text-center hover:border-blue-500 cursor-pointer transition-all duration-300 bg-white/50 dark:bg-gray-800/50 flex flex-col items-center justify-center">
                                    <input
                                        type="file"
                                        id="resume-upload"
                                        accept=".pdf,.docx,.txt"
                                        onChange={(e) =>
                                            handleFileInput(e, "resume")
                                        }
                                        className="hidden"
                                    />
                                    <label
                                        htmlFor="resume-upload"
                                        className="cursor-pointer"
                                    >
                                        <Upload className="mx-auto h-12 w-12 text-blue-500 mb-4" />
                                        <h3 className="text-lg font-semibold mb-2">
                                            Upload your resume
                                        </h3>
                                        <p className="text-sm text-gray-500 mb-2">
                                            Drop your PDF, DOCX, or TXT file
                                            here, or click to browse
                                        </p>
                                        {resumeFile && (
                                            <Alert className="mt-4">
                                                <FileText className="h-4 w-4" />
                                                <AlertTitle>
                                                    File uploaded
                                                </AlertTitle>
                                                <AlertDescription>
                                                    {resumeFile.name}
                                                </AlertDescription>
                                            </Alert>
                                        )}
                                    </label>
                                </div>
                            ) : (
                                <Textarea
                                    placeholder="Paste your resume text here..."
                                    className="h-full resize-none bg-white/50 dark:bg-gray-800/50"
                                    value={resumeText}
                                    onChange={(e) =>
                                        setResumeText(e.target.value)
                                    }
                                    onPaste={(e) => handlePaste(e, "resume")}
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
                                variant={
                                    jobActiveTab === "upload"
                                        ? "default"
                                        : "outline"
                                }
                                onClick={() => setJobActiveTab("upload")}
                                className="flex-1"
                            >
                                <Upload className="h-4 w-4 mr-2" />
                                Upload
                            </Button>
                            <Button
                                variant={
                                    jobActiveTab === "paste"
                                        ? "default"
                                        : "outline"
                                }
                                onClick={() => setJobActiveTab("paste")}
                                className="flex-1"
                            >
                                <ClipboardPaste className="h-4 w-4 mr-2" />
                                Paste
                            </Button>
                        </div>

                        <div
                            onDragOver={handleDragOver}
                            onDragLeave={handleDragLeave}
                            onDrop={(e) => handleDrop(e, "job")}
                            className="h-[400px] overflow-y-auto"
                        >
                            {jobActiveTab === "upload" ? (
                                <div className="h-full border-2 border-dashed rounded-lg p-8 text-center hover:border-purple-500 cursor-pointer transition-all duration-300 bg-white/50 dark:bg-gray-800/50 flex flex-col items-center justify-center">
                                    <input
                                        type="file"
                                        id="jd-upload"
                                        accept=".pdf,.docx,.txt"
                                        onChange={(e) =>
                                            handleFileInput(e, "job")
                                        }
                                        className="hidden"
                                    />
                                    <label
                                        htmlFor="jd-upload"
                                        className="cursor-pointer"
                                    >
                                        <Upload className="mx-auto h-12 w-12 text-purple-500 mb-4" />
                                        <h3 className="text-lg font-semibold mb-2">
                                            Upload job description
                                        </h3>
                                        <p className="text-sm text-gray-500 mb-2">
                                            Drop your PDF, DOCX, or TXT file
                                            here, or click to browse
                                        </p>
                                        {jobFile && (
                                            <Alert className="mt-4">
                                                <FileText className="h-4 w-4" />
                                                <AlertTitle>
                                                    File uploaded
                                                </AlertTitle>
                                                <AlertDescription>
                                                    {jobFile.name}
                                                </AlertDescription>
                                            </Alert>
                                        )}
                                    </label>
                                </div>
                            ) : (
                                <Textarea
                                    placeholder="Paste your job description here..."
                                    className="h-full resize-none bg-white/50 dark:bg-gray-800/50"
                                    value={jobText}
                                    onChange={(e) => setJobText(e.target.value)}
                                    onPaste={(e) => handlePaste(e, "job")}
                                />
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
                                        disabled={
                                            isAnalyzing ||
                                            (!resumeFile && !resumeText) ||
                                            (!jobFile && !jobText)
                                        }
                                        className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-8 py-6 text-lg"
                                    >
                                        {isAnalyzing ? (
                                            <>
                                                <Loader2 className="h-5 w-5 mr-2 animate-spin" />
                                                Analyzing...
                                            </>
                                        ) : (
                                            <>
                                                <Sparkles className="h-5 w-5 mr-2" />
                                                Analyze Resume
                                            </>
                                        )}
                                    </Button>
                                </span>
                            </TooltipTrigger>
                            <TooltipContent>
                                {(!resumeFile && !resumeText) ||
                                (!jobFile && !jobText)
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
