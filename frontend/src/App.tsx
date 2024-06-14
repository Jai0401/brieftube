import './App.css'
import { useState } from 'react'
import axios from 'axios';
import VideoSummary from './components/Summary';

function App() {
  const [url, setUrl] = useState<string>('')
  const [summary, setSummary] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const handleSubmit = () => {
    console.log(url);
    setLoading(true);
    axios.post('http://127.0.0.1:5000/get_summary', {youtube_link: url})
    .then(res => {
      console.log(res.data);
      setSummary(res.data.video_summary);
      setLoading(false);
    })
  }

  return (
    <>
      <h1>BriefTube</h1>
      <p >YouTube video summariser</p>
      <input type="text" value={url} placeholder="Paste a YouTube URL" onChange={(e)=>setUrl(e.target.value)}/>
      <button onClick={handleSubmit}>Submit</button>
      {loading ?<><br/>Loading...</> : summary ? (
        <>
          <VideoSummary summary={summary}/>
        </>
      ): null}
    </>
  )
}

export default App
