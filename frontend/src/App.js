import './App.css';
import logo from './RutgersVax.png'
import React, {useState, useEffect} from 'react';
import validator from 'validator';
import { Button, Form, FormGroup, Label, Input, Jumbotron, Fade, Row } from 'reactstrap';
const axios = require("axios")

function App() {
  const [cities, setcities] = useState([])
  const [selection, setselection] = useState([])
  const [error, seterror] = useState('')

  const [fadeIn, setFadeIn] = useState(false);

  const toggle = () => setFadeIn(!fadeIn);
  
  var phoneNumber = ""

  useEffect(()=>{
    getCities();
  }, [])

  async function getCities(){
    axios.get("https://www.cvs.com/immunizations/covid-19-vaccine/immunizations/covid-19-vaccine.vaccine-status.NJ.json?vaccineinfo",{
    }).then(res => {
      let x = res.data['responsePayloadData']['data']['NJ'];
      var list = [];
      for(let i=0; i<x.length; i++){
        list.push(x[i].city)
      }
      setcities(list);
    }).catch(err => {
      console.log(err)
    })
  } 

  const removeSelection = (toRemove) =>{
    var temp = [];
    for(var city of selection){
      if(city !== toRemove){
        temp.push(city);
      }
    }
    setselection(temp)
  }

  const updatePhone = (phone) =>{
    phoneNumber = phone.target.value;
  }

  const addToDatabase = (e) =>{
    e.preventDefault()

    if(!validator.isMobilePhone(phoneNumber, 'en-US')){
      phoneNumber = '';
      alert("Invalid Phone Number");
      seterror("Invalid Phone Number");
      return;
    }

    console.log(phoneNumber)
    axios.post(`/newnumber`,{
      phone: phoneNumber,
      cities: selection
    })
    window.location.reload();
  }

  return (
    <div>
      
      <div className="App">
        <Jumbotron style={{width:'100vh', marginTop:'-20%', marginBottom:'-5%'}} className="Info">
          <Row>
            <img className="logo" alt="logo" src={logo}/>
            <h1 style={{marginLeft:'150px'}} className="display-3">RU VAXXED?</h1>
          </Row>
          <p className="lead">Select cities that you want to be notified for vaccine appointments</p>
          <hr color="white" className="my-2" />
          <p className="lead">You will be notified by text when an appointment becomes available</p>
          <p className="lead">
            <Button style={{backgroundColor:'#87cefa'}} onClick={toggle} >Subscribe</Button>
          </p>
        </Jumbotron>
        <Fade in={fadeIn} tag="h5" className="mt-3">
            
          <FormGroup style={{textAlign:'center'}}>
            <Label for="exampleSelectMulti">Select Cities in NJ</Label>
            <Input style={{height:"40vh"}} type="select" name="selectMulti" id="selectMulti" multiple>
              {
                cities.map((city) =>
                  selection.includes(city)?
                  <option style={{backgroundColor:'lightgray'}} onClick={() =>{removeSelection(city)}} key={city}>{city}</option>:
                  <option onClick={()=>{setselection([...selection,city])}} key={city}>{city}</option>
                )
              }
            </Input>
          </FormGroup>
          
          <Form inline onSubmit={addToDatabase}>
            <FormGroup className="mb-2 mr-sm-2 mb-sm-0">
              {/* <Label style={{marginLeft:50}} for="number" className="mr-sm-2">Phone Number</Label> */}
              <Input onChange={updatePhone} type="tel" name="number" id="number" style={error===''?{}:{border:'2px solid red'}} placeholder={error===''?"Enter Phone Number":error}/>
            </FormGroup>  
            <Button style={{backgroundColor:'#87cefa'}}>Submit</Button>
          </Form>
        </Fade>
      </div>
    </div>
  );
}

export default App;
