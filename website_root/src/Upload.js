import React, { useState } from 'react';
import axios from 'axios';
import { Container, Row, Col, Form, Button, Image } from 'react-bootstrap';

const apiURL =  "https://lubomyr-ai-api-b1f15885f038.herokuapp.com/ai/predict";
const Upload = () => {
  
    const [file1, setFile1] = useState(null);
    const [file2, setFile2] = useState(null);
    const [apiResponse, setApiResponse] = useState('');
    
    const handleFile1Change = (event) => {
      setApiResponse("");
      setFile1(event.target.files[0]);
      if(event.target.files[0]==null){
        document.getElementById('delButton1').hidden=true;
      }
      else{
        document.getElementById('delButton1').hidden=false;
      }
    };
  
    const handleFile2Change = (event) => {
      setApiResponse("");
      setFile2(event.target.files[0]);
      if(event.target.files[0]==null){
        document.getElementById('delButton2').hidden=true;
      }
      else{
        document.getElementById('delButton2').hidden=false;
      }
    };
    const handleDel1 = (event) => {
      setApiResponse("");      
      setFile1(null);
      document.getElementById("file1").value = null;
      document.getElementById('delButton1').hidden=true;
    }
    const handleDel2 = (event) => {
      setApiResponse("");
      setFile2(null);
      document.getElementById("file2").value = null;
      document.getElementById('delButton2').hidden=true;
    }
    const handleUpload = () => {
      
      if (!file1 || !file2) {
        setApiResponse('Please select files for both inputs');
        return;
      }
  
      const readAsBase64 = (file) => {
        return new Promise((resolve, reject) => {
          const reader = new FileReader();
          reader.onloadend = () => resolve(reader.result.split(',')[1]);
          reader.onerror = reject;
          reader.readAsDataURL(file);
        });
      };
    
      const uploadImages = async () => {
        try {
          const base64File1 = await readAsBase64(file1);
          const base64File2 = await readAsBase64(file2);
    
          const requestBody = {
            "modelId": "sift",
            "image1": base64File1,
            "image2": base64File2
          };
          
          const response = await axios.post(apiURL, requestBody, 
            
          );
          
          setApiResponse(response.request.responseText);
        } catch (error) {
          setApiResponse("An error has occured!");
          console.error('Error uploading files:', error);
        }
      };
    
      uploadImages();
    };
  
    return (
      <Container>
        <Row className='mt-5 mb-3'>
          <Col xs={6}>
            <Form.Group >
              <Form.Label>Photo 1</Form.Label>
              <Form.Control id="file1" type="file" onChange={handleFile1Change} />
              
            </Form.Group>
            {file1 && (
              <Image className='mt-2'
                src={URL.createObjectURL(file1)}
                alt="File 1 Preview"
                fluid
                style={{ border: '2px solid #ddd', borderRadius: '8px', maxHeight: '150px',minHeight: '150px' }}
              />
              
            )}
          </Col>
          <Col xs={6} className='justify-content-center'>
            <Form.Group >
              <Form.Label>Photo 2</Form.Label>
              <Form.Control type="file" id="file2" onChange={handleFile2Change} />
            </Form.Group>
            {file2 && (
              <Image className='mt-2 '
                src={URL.createObjectURL(file2)}
                alt="File 2 Preview"
                fluid
                style={{ border: '2px solid #ddd', borderRadius: '8px', maxHeight: '150px',minHeight: '150px'  }}
              />
            )}
          </Col>
        </Row>
        <Row className='mt-2 mb-2'>
          <Col xs={6}>
            <Button variant='danger' hidden='true'id='delButton1'onClick={handleDel1}>X</Button>
          </Col>
          <Col xs={6}>
            <Button variant='danger'hidden='true' id='delButton2'onClick={handleDel2}>X</Button>
          </Col>
        </Row>
        <Row className="justify-content-center">
          <Button variant="primary" onClick={handleUpload}>Upload</Button>
        </Row>
        <Row className="mt-3 justify-content-center"><p>Result: {apiResponse}</p></Row>
      </Container>
    );
  };

export default Upload;
