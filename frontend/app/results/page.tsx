"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import {
    ArrowLeft,
    Download,
    FileText,
    Calendar,
    ChevronUp,
} from "lucide-react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { ScoreResponse } from "@/lib/api";
import ReactECharts from "echarts-for-react";

const getScoreLabel = (score: number): string => {
    if (score >= 80) return "Excellent";
    if (score >= 60) return "Good";
    return "Needs Work";
};

const getScoreColor = (score: number): string => {
    if (score >= 80) return "bg-emerald-500";
    if (score >= 60) return "bg-amber-500";
    return "bg-rose-500";
};

const getBadgeVariant = (
    score: number
): "default" | "secondary" | "outline" => {
    if (score >= 80) return "default";
    if (score >= 60) return "secondary";
    return "outline";
};

const OverallScore = ({ score }: { score: number }) => {
    const previousScore = score - 7; // Mock previous score
    const improvement = (
        ((score - previousScore) / previousScore) *
        100
    ).toFixed(1);

    return (
        <Card className="p-6 bg-white">
            <div className="flex justify-between items-start mb-4">
                <div>
                    <h3 className="text-lg font-medium text-gray-700">
                        Overall Match Score
                    </h3>
                    <p className="text-sm text-gray-500">Updated today</p>
                </div>
                <Badge
                    variant={getBadgeVariant(score)}
                    className="flex items-center gap-1"
                >
                    <ChevronUp className="h-3 w-3" />
                    {improvement}% Improvement
                </Badge>
            </div>
            <div className="flex items-end space-x-4 mb-4">
                <div className="text-5xl font-bold text-indigo-600">
                    {Math.round(score)}
                </div>
                <div className="text-2xl font-medium text-gray-400">/100</div>
            </div>
            <Progress value={score} className="h-2" />
        </Card>
    );
};

const DetailedMetrics = ({ results }: { results: ScoreResponse }) => {
    const metrics = [
        {
            category: "Keyword Matching",
            current: Math.round(results.tfidf_score),
            previous: Math.round(results.tfidf_score - 5),
            description:
                "Measures how well your resume matches the required keywords",
            improvements: [
                {
                    score: 60,
                    action: "Add more job-specific keywords from the job description",
                },
                {
                    score: 75,
                    action: "Include industry-standard tools and technologies",
                },
                {
                    score: 85,
                    action: "Fine-tune keyword placement in key sections",
                },
            ],
        },
        {
            category: "Contextual Similarity",
            current: Math.round(results.word2vec_score),
            previous: Math.round(results.word2vec_score - 3),
            description:
                "Evaluates how well your experience aligns with the job context",
            improvements: [
                {
                    score: 60,
                    action: "Add more relevant work experience examples",
                },
                {
                    score: 75,
                    action: "Highlight projects that match job requirements",
                },
                {
                    score: 85,
                    action: "Emphasize leadership and team contributions",
                },
            ],
        },
        {
            category: "Semantic Understanding",
            current: Math.round(results.sbert_score),
            previous: Math.round(results.sbert_score - 4),
            description:
                "Analyzes the overall meaning and relevance of your qualifications",
            improvements: [
                {
                    score: 60,
                    action: "Better align your experience with job requirements",
                },
                {
                    score: 75,
                    action: "Add measurable achievements and outcomes",
                },
                {
                    score: 85,
                    action: "Enhance role descriptions to match job level",
                },
            ],
        },
    ];

    return (
        <Card className="p-6 bg-white">
            <h3 className="text-lg font-medium text-gray-700 mb-6">
                Detailed Metrics
            </h3>
            <div className="space-y-4">
                {metrics.map((metric, index) => (
                    <div key={index} className="p-4 bg-gray-50 rounded-lg">
                        <div className="flex items-center justify-between mb-4">
                            <div>
                                <h4 className="font-medium text-gray-900">
                                    {metric.category}
                                </h4>
                                <div className="flex items-center space-x-2 mt-1">
                                    <span className="text-sm text-gray-500">
                                        Previous: {metric.previous}
                                    </span>
                                    <ChevronUp className="h-3 w-3 text-emerald-500" />
                                </div>
                                <p className="text-sm text-gray-500 mt-1">
                                    {metric.description}
                                </p>
                            </div>
                            <div className="flex items-center space-x-4">
                                <Progress
                                    value={metric.current}
                                    className="w-32"
                                />
                                <span className="font-medium text-gray-900">
                                    {metric.current}%
                                </span>
                            </div>
                        </div>

                        {/* Improvement Suggestions */}
                        {metric.current < 90 && (
                            <div className="mt-4 border-t border-gray-200 pt-4">
                                <h5 className="text-sm font-medium text-gray-700 mb-2">
                                    Suggested Improvements
                                </h5>
                                <ul className="space-y-2">
                                    {metric.improvements
                                        .filter(
                                            (imp) => metric.current <= imp.score
                                        )
                                        .slice(0, 2)
                                        .map((improvement, i) => (
                                            <li
                                                key={i}
                                                className="flex items-start gap-2 text-sm text-gray-600"
                                            >
                                                <div className="min-w-[6px] h-[6px] mt-[6px] rounded-full bg-indigo-500" />
                                                {improvement.action}
                                            </li>
                                        ))}
                                </ul>
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </Card>
    );
};

const ScoreHistory = ({ results }: { results: ScoreResponse }) => {
    const options = {
        animation: false,
        grid: {
            top: 40,
            right: 20,
            bottom: 40,
            left: 50,
        },
        xAxis: {
            type: "category",
            data: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            axisLine: { lineStyle: { color: "#94a3b8" } },
        },
        yAxis: {
            type: "value",
            min: 0,
            max: 100,
            axisLine: { lineStyle: { color: "#94a3b8" } },
        },
        series: [
            {
                data: [65, 70, 72, 78, 82, Math.round(results.combined_score)],
                type: "line",
                smooth: true,
                lineStyle: { color: "#6366f1" },
                areaStyle: {
                    color: {
                        type: "linear",
                        x: 0,
                        y: 0,
                        x2: 0,
                        y2: 1,
                        colorStops: [
                            { offset: 0, color: "rgba(99, 102, 241, 0.2)" },
                            { offset: 1, color: "rgba(99, 102, 241, 0)" },
                        ],
                    },
                },
            },
        ],
    };

    return (
        <Card className="p-6 bg-white">
            <h3 className="text-lg font-medium text-gray-700 mb-4">
                Score History
            </h3>
            <ReactECharts option={options} style={{ height: "200px" }} />
        </Card>
    );
};

export default function ResultsPage() {
    const router = useRouter();
    const [results, setResults] = useState<ScoreResponse | null>(null);

    useEffect(() => {
        const storedResults = localStorage.getItem("atsResults");
        if (storedResults) {
            setResults(JSON.parse(storedResults));
        }
    }, []);

    if (!results) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-gray-50">
                <Card className="p-8 text-center bg-white">
                    <h2 className="text-2xl font-bold mb-4 text-gray-900">
                        No Results Found
                    </h2>
                    <p className="text-gray-500 mb-6">
                        Please analyze a resume first.
                    </p>
                    <Button
                        onClick={() => router.push("/")}
                        variant="outline"
                        className="gap-2"
                    >
                        <ArrowLeft className="h-4 w-4" />
                        Back to Analysis
                    </Button>
                </Card>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
                <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
                    <Button
                        variant="ghost"
                        onClick={() => router.push("/")}
                        className="gap-2"
                    >
                        <ArrowLeft className="h-4 w-4" />
                        Back to Analysis
                    </Button>
                    <div className="flex items-center gap-4">
                        <div className="text-sm text-gray-500 flex items-center gap-2">
                            <Calendar className="h-4 w-4" />
                            {new Date(
                                results?.calculated_at || ""
                            ).toLocaleString()}
                        </div>
                        <Button className="gap-2">
                            <Download className="h-4 w-4" />
                            Export Report
                        </Button>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-4 py-8">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                    <OverallScore score={results.combined_score} />
                    <div className="md:col-span-2">
                        <ScoreHistory results={results} />
                    </div>
                </div>

                <div className="grid grid-cols-1 gap-6">
                    <DetailedMetrics results={results} />
                </div>
            </main>
        </div>
    );
}
