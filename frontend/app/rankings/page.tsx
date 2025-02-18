"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { ArrowLeft, Trophy, FileText, Search } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import { Progress } from "@/components/ui/progress";
import { ScoreResponse, getRankings } from "@/lib/api";
import { useToast } from "@/hooks/use-toast";

interface RankedScore extends ScoreResponse {
    rank: number;
}

export default function RankingsPage() {
    const router = useRouter();
    const [scores, setScores] = useState<RankedScore[]>([]);
    const [searchTerm, setSearchTerm] = useState("");
    const [isLoading, setIsLoading] = useState(true);
    const [selectedJobId, setSelectedJobId] = useState<string | undefined>();
    const { toast } = useToast();

    useEffect(() => {
        fetchRankings();
    }, [selectedJobId]);

    const fetchRankings = async () => {
        try {
            setIsLoading(true);
            const response = await getRankings(selectedJobId);

            // Add rank to each score based on combined_score
            const rankedScores = response.scores
                .sort((a, b) => b.combined_score - a.combined_score)
                .map((score, index) => ({
                    ...score,
                    rank: index + 1,
                }));

            setScores(rankedScores);
        } catch (error) {
            toast({
                title: "Error",
                description: "Failed to fetch rankings. Please try again.",
                variant: "destructive",
            });
        } finally {
            setIsLoading(false);
        }
    };

    const filteredScores = scores.filter(
        (score) =>
            score.resume_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
            score.job_id.toLowerCase().includes(searchTerm.toLowerCase())
    );

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
            <div className="max-w-7xl mx-auto">
                <Button
                    variant="outline"
                    onClick={() => router.push("/")}
                    className="mb-8"
                >
                    <ArrowLeft className="h-4 w-4 mr-2" />
                    Back to Analysis
                </Button>

                <div className="flex justify-between items-center mb-8">
                    <h1 className="text-4xl font-bold flex items-center gap-3">
                        <Trophy className="h-8 w-8 text-yellow-500" />
                        Resume Rankings
                    </h1>
                    <div className="flex gap-4">
                        <Button
                            variant={selectedJobId ? "outline" : "default"}
                            onClick={() => setSelectedJobId(undefined)}
                        >
                            All Jobs
                        </Button>
                        <div className="relative w-64">
                            <Search className="absolute left-2 top-2.5 h-4 w-4 text-gray-500" />
                            <Input
                                placeholder="Search resumes or jobs..."
                                className="pl-8"
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                            />
                        </div>
                    </div>
                </div>

                <Card className="p-6">
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead className="w-20">Rank</TableHead>
                                <TableHead>Resume ID</TableHead>
                                <TableHead>Job ID</TableHead>
                                <TableHead className="text-right">
                                    TF-IDF Score
                                </TableHead>
                                <TableHead className="text-right">
                                    Word2Vec Score
                                </TableHead>
                                <TableHead className="text-right">
                                    SBERT Score
                                </TableHead>
                                <TableHead className="text-right">
                                    Combined Score
                                </TableHead>
                                <TableHead className="text-right">
                                    Analyzed At
                                </TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {isLoading ? (
                                <TableRow>
                                    <TableCell
                                        colSpan={8}
                                        className="text-center py-8"
                                    >
                                        Loading rankings...
                                    </TableCell>
                                </TableRow>
                            ) : filteredScores.length === 0 ? (
                                <TableRow>
                                    <TableCell
                                        colSpan={8}
                                        className="text-center py-8"
                                    >
                                        No resumes found
                                    </TableCell>
                                </TableRow>
                            ) : (
                                filteredScores.map((score) => (
                                    <TableRow
                                        key={`${score.resume_id}-${score.job_id}`}
                                    >
                                        <TableCell className="font-medium">
                                            {score.rank === 1 ? (
                                                <Trophy className="h-5 w-5 text-yellow-500" />
                                            ) : (
                                                score.rank
                                            )}
                                        </TableCell>
                                        <TableCell className="flex items-center gap-2">
                                            <FileText className="h-4 w-4" />
                                            {score.resume_id}
                                        </TableCell>
                                        <TableCell>
                                            <Button
                                                variant="ghost"
                                                className="p-0 h-auto hover:bg-transparent"
                                                onClick={() =>
                                                    setSelectedJobId(
                                                        score.job_id
                                                    )
                                                }
                                            >
                                                {score.job_id}
                                            </Button>
                                        </TableCell>
                                        <TableCell
                                            className={`text-right ${getScoreColor(
                                                score.tfidf_score
                                            )}`}
                                        >
                                            {score.tfidf_score.toFixed(1)}%
                                        </TableCell>
                                        <TableCell
                                            className={`text-right ${getScoreColor(
                                                score.word2vec_score
                                            )}`}
                                        >
                                            {score.word2vec_score.toFixed(1)}%
                                        </TableCell>
                                        <TableCell
                                            className={`text-right ${getScoreColor(
                                                score.sbert_score
                                            )}`}
                                        >
                                            {score.sbert_score.toFixed(1)}%
                                        </TableCell>
                                        <TableCell
                                            className={`text-right ${getScoreColor(
                                                score.combined_score
                                            )}`}
                                        >
                                            {score.combined_score.toFixed(1)}%
                                        </TableCell>
                                        <TableCell className="text-right">
                                            {new Date(
                                                score.calculated_at
                                            ).toLocaleString()}
                                        </TableCell>
                                    </TableRow>
                                ))
                            )}
                        </TableBody>
                    </Table>
                </Card>
            </div>
        </main>
    );
}
