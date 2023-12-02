import React, { useState } from 'react';
import axios from 'axios';
import { Container, Row, Col, Form, Button, Image } from 'react-bootstrap';

const Upload = () => {
    const [file1, setFile1] = useState(null);
    const [file2, setFile2] = useState(null);
    const [apiResponse, setApiResponse] = useState('');
    const apiUTL = process.env.FILES_UPLOAD_URL ||  'http://127.0.0.1:5000/upload';
    const handleFile1Change = (event) => {
      setFile1(event.target.files[0]);
    };
  
    const handleFile2Change = (event) => {
      setFile2(event.target.files[0]);
    };
  
    const handleUpload = () => {
      if (!file1 || !file2) {
        setApiResponse('Please select files for both inputs');
        return;
      }
  
      const formData = new FormData();
      formData.append('file1', file1);
      formData.append('file2', file2);
  
      axios.post(, formData)
        .then(response => {
            var temp = response.data['message'];
            setApiResponse(temp);
        })
        .catch(error => {
            console.error('Error uploading files:', error);
        });
    };
  
    return (
      <Container>
        <Row className='pt-5 pb-3'>
          <Col xs={6}>
            <Form.Group controlId="file1">
              <Form.Label>Photo 1</Form.Label>
              <Form.Control type="file" onChange={handleFile1Change} />
            </Form.Group>
            {file1 && (
              <Image
                src={URL.createObjectURL(file1)}
                alt="File 1 Preview"
                fluid
                style={{ border: '2px solid #ddd', borderRadius: '8px', maxHeight: '150px',minHeight: '150px' }}
              />
            )}
          </Col>
          <Col xs={6}>
            <Form.Group controlId="file2">
              <Form.Label>Photo 2</Form.Label>
              <Form.Control type="file" onChange={handleFile2Change} />
            </Form.Group>
            {file2 && (
              <Image
                src={URL.createObjectURL(file2)}
                alt="File 2 Preview"
                fluid
                style={{ border: '2px solid #ddd', borderRadius: '8px', maxHeight: '150px',minHeight: '150px'  }}
              />
            )}
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
