import './App.css';
import { useState, useEffect } from 'react';
import Charts from './components/Charts/Charts';
import { Button } from '@mui/material';
import { styled } from '@mui/material/styles';
import Papa from 'papaparse';



function App() {
  const [reviews, setReviews] = useState([])
  const [charts, setCharts] = useState(<div className="spinner"/>)
  const [hideButton, setHideButton] = useState(false)
  const [fileUploadData, setFileUploadData] = useState(null)
  const VisuallyHiddenInput = styled('input')({
    clip: 'rect(0 0 0 0)',
    clipPath: 'inset(50%)',
    height: 1,
    overflow: 'hidden',
    position: 'absolute',
    bottom: 0,
    left: 0,
    whiteSpace: 'nowrap',
    width: 1,
  });

  function handleFile(e){
    setHideButton(true)
    Papa.parse(e.target.files[0], {
      header: true,
      skipEmptyLines: true,
      complete: function (results) {
        console.log(results.data)
        fetch('http://localhost:5000/reviews', {
          method: "POST",
          body: JSON.stringify(results.data)
        }).then(response => {
          response.json().then(json =>{
            setCharts(<Charts data ={json}/>)
          })
        })
      },
    });
    
  }

  useEffect(() => {

    const form = document.getElementById("fileUploadForm");
    const data = new FormData(form);
    setFileUploadData(data)
    //fetch('http://localhost:5000/reviews', {
      //method: "GET"
    //}).then(response =>{
      //response.json().then(data =>{
        //setReviews(data)
        //setCharts(<Charts data ={data}/>)
      //})
    //})
  //
  }, [])
  return (
    
    <div className="App">
      <div className='main-container'>
        <div className='button-container' hidden={hideButton}>
        <form id="fileUploadForm" className='file-upload'>
          <Button
          component="label"
          role={undefined}
          variant="contained"
          tabIndex={-1}
          >
            Upload file
            <VisuallyHiddenInput type="file" onChange={handleFile}/>
          </Button>
        </form>
        </div>
        <div className='chart-container' hidden={!hideButton}>
          {charts}
        </div>
      </div>
    </div>
  );
}

export default App;
