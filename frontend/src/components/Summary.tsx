// Helper function to parse the summary using regex
const parseSummary = (summary: string): { [key: string]: string } => {
    const sectionRegex = /\*\*(.*?)\*\*:(.*?)(?=\*\*|$)/gs;
    const parsedSections: { [key: string]: string } = {};
  
    let match;
    while ((match = sectionRegex.exec(summary)) !== null) {
      const title = match[1].trim();
      const content = match[2].trim().replace(/\n/g, ' ');
      parsedSections[title] = content;
    }
  
    return parsedSections;
  };
  
  // React component
  interface VideoSummaryProps {
    summary: string;
  }
  
  const VideoSummary: React.FC<VideoSummaryProps> = ({ summary }) => {
    const parsedSummary = parseSummary(summary);
  
    return (
      <div>
        <h1>{parsedSummary['Title']}</h1>
        {parsedSummary['Introduction'] && (
          <section>
            <h2>Introduction</h2>
            <p>{parsedSummary['Introduction']}</p>
          </section>
        )}
        {parsedSummary['Key Points'] && (
          <section>
            <h2>Key Points</h2>
            <ul>
              {parsedSummary['Key Points'].split('-').map((point, index) => (
                <li key={index}>{point.trim()}</li>
              ))}
            </ul>
          </section>
        )}
        {parsedSummary['Examples'] && (
          <section>
            <h2>Examples</h2>
            <p>{parsedSummary['Examples']}</p>
          </section>
        )}
        {parsedSummary['Benefits and Impact'] && (
          <section>
            <h2>Benefits and Impact</h2>
            <p>{parsedSummary['Benefits and Impact']}</p>
          </section>
        )}
        {parsedSummary['Conclusion'] && (
          <section>
            <h2>Conclusion</h2>
            <p>{parsedSummary['Conclusion']}</p>
          </section>
        )}
      </div>
    );
  };
  
  export default VideoSummary;
