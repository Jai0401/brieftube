import './App.css'
import { useState } from 'react'
import axios from 'axios';

function App() {
  const [url, setUrl] = useState<string>('')
  const [summary, setSummary] = useState<string | null>(null);
  const [title, setTitle] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const handleSubmit = () => {
    console.log(url);
    setLoading(true);
    axios.post('https://brieftube-1.onrender.com', {youtube_link: url})
    .then(res => {
      console.log(res.data);
      setSummary(res.data.summary);
      setTitle(res.data.title);
      setLoading(false);
    })
    .catch(err => {
      alert(err.response.data.error);
      setLoading(false);
    })
  }

  return (
    <div className='m-6'>
      <h1 className='text-center text-2xl'>BriefTube</h1>
      <p className='text-center text-lg p-4'>YouTube video summariser</p>
      <div className='flex justify-center p-4'>
      <input type="text" value={url} placeholder="Paste a YouTube URL" onChange={(e)=>setUrl(e.target.value)}
      className='w-96 h-10 mr-2 border-black border-2 align-middle rounded-md px-2'/>
      <button onClick={handleSubmit} className="border-black border-2 p-2 h-10 rounded-md hover:text-white hover:bg-black">Submit</button>
      </div>
      {loading ?
      <div className='text-center text-lg p-4'>Loading...</div> : summary ? (
        <div className='flex justify-center'>
        <div className='pt-8 w-3/4'>
          <h1 className='text-xl font-bold'>{title}</h1>
          <p>{summary}</p>
        </div>
        </div>
      ): null}
    </div>
  )
}

export default App
