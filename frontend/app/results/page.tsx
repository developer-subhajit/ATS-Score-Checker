"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { ArrowLeft, FileText, BarChart2, Target } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { ScoreResponse } from "@/lib/api";

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
            <div className="min-h-screen flex items-center justify-center">
                <Card className="p-8 text-center">
                    <h2 className="text-2xl font-bold mb-4">
                        No Results Found
                    </h2>
                    <p className="text-gray-600 mb-4">
                        Please analyze a resume first.
                    </p>
                    <Button onClick={() => router.push("/")}>
                        <ArrowLeft className="h-4 w-4 mr-2" />
                        Back to Analysis
                    </Button>
                </Card>
            </div>
        );
    }

    const getScoreColor = (score: number) => {
        if (score >= 80) return "text-green-500";
        if (score >= 60) return "text-yellow-500";
        return "text-red-500";
    };

    const getProgressColor = (score: number) => {
        if (score >= 80) return "bg-green-500";
        if (score >= 60) return "bg-yellow-500";
        return "bg-red-500";
    };

    return (
        <main className="min-h-screen bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-blue-100 via-blue-50 to-white dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-5xl mx-auto">
                <Button
                    variant="outline"
                    onClick={() => router.push("/")}
                    className="mb-8"
                >
                    <ArrowLeft className="h-4 w-4 mr-2" />
                    Back to Analysis
                </Button>

                <h1 className="text-4xl font-bold mb-8">Analysis Results</h1>

                <div className="grid gap-8 md:grid-cols-2">
                    {/* Combined Score */}
                    <Card className="p-6 col-span-2">
                        <div className="flex items-center gap-2 mb-4">
                            <Target className="h-6 w-6 text-blue-500" />
                            <h2 className="text-2xl font-semibold">
                                Overall Match Score
                            </h2>
                        </div>
                        <div className="flex items-center gap-4 mb-4">
                            <div
                                className={`text-5xl font-bold ${getScoreColor(
                                    results.combined_score
                                )}`}
                            >
                                {Math.round(results.combined_score)}%
                            </div>
                            <Progress
                                value={results.combined_score}
                                className="flex-1"
                                indicatorClassName={getProgressColor(
                                    results.combined_score
                                )}
                            />
                        </div>
                    </Card>

                    {/* Individual Scores */}
                    <Card className="p-6">
                        <div className="flex items-center gap-2 mb-4">
                            <FileText className="h-6 w-6 text-purple-500" />
                            <h2 className="text-xl font-semibold">
                                Keyword Matching
                            </h2>
                        </div>
                        <div className="space-y-4">
                            <div>
                                <div className="flex justify-between mb-2">
                                    <span>TF-IDF Score</span>
                                    <span
                                        className={getScoreColor(
                                            results.tfidf_score
                                        )}
                                    >
                                        {Math.round(results.tfidf_score)}%
                                    </span>
                                </div>
                                <Progress
                                    value={results.tfidf_score}
                                    className="w-full"
                                    indicatorClassName={getProgressColor(
                                        results.tfidf_score
                                    )}
                                />
                            </div>
                            <div>
                                <div className="flex justify-between mb-2">
                                    <span>Word2Vec Score</span>
                                    <span
                                        className={getScoreColor(
                                            results.word2vec_score
                                        )}
                                    >
                                        {Math.round(results.word2vec_score)}%
                                    </span>
                                </div>
                                <Progress
                                    value={results.word2vec_score}
                                    className="w-full"
                                    indicatorClassName={getProgressColor(
                                        results.word2vec_score
                                    )}
                                />
                            </div>
                        </div>
                    </Card>

                    <Card className="p-6">
                        <div className="flex items-center gap-2 mb-4">
                            <BarChart2 className="h-6 w-6 text-green-500" />
                            <h2 className="text-xl font-semibold">
                                Semantic Matching
                            </h2>
                        </div>
                        <div>
                            <div className="flex justify-between mb-2">
                                <span>SBERT Score</span>
                                <span
                                    className={getScoreColor(
                                        results.sbert_score
                                    )}
                                >
                                    {Math.round(results.sbert_score)}%
                                </span>
                            </div>
                            <Progress
                                value={results.sbert_score}
                                className="w-full"
                                indicatorClassName={getProgressColor(
                                    results.sbert_score
                                )}
                            />
                        </div>
                    </Card>
                </div>

                <div className="mt-8 text-sm text-gray-500">
                    Analysis completed at:{" "}
                    {new Date(results.calculated_at).toLocaleString()}
                </div>
            </div>
        </main>
    );
}
