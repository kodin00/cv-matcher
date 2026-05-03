import { useState } from 'react';
import { FileUpload } from '@/components/FileUpload';
import { JobManager } from '@/components/JobManager';
import { MatchButton } from '@/components/MatchButton';
import { MatchResults } from '@/components/MatchResults';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Briefcase, User, Sparkles } from 'lucide-react';

function App() {
  const [resultsOpen, setResultsOpen] = useState(false);

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b bg-card">
        <div className="w-full px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Sparkles className="h-6 w-6 text-primary" />
              <h1 className="text-xl font-bold">CV Matcher</h1>
            </div>
            <MatchButton onMatchComplete={() => setResultsOpen(true)} />
          </div>
        </div>
      </header>

      <main className="w-full px-6 py-6">
        {/* Two columns: CV (Left) | Job (Right) */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left Column - CV Upload */}
          <Card className="h-fit">
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <User className="h-5 w-5" />
                Candidate CV
              </CardTitle>
            </CardHeader>
            <CardContent>
              <FileUpload />
            </CardContent>
          </Card>

          {/* Right Column - Job Description */}
          <Card className="h-fit">
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <Briefcase className="h-5 w-5" />
                Job Description
              </CardTitle>
            </CardHeader>
            <CardContent>
              <JobManager />
            </CardContent>
          </Card>
        </div>
      </main>

      {/* Results Popup */}
      <MatchResults open={resultsOpen} onOpenChange={setResultsOpen} />
    </div>
  );
}

export default App;
