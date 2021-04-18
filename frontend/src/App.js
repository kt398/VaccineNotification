import './App.css';
import React, {useState, useEffect} from 'react';
import { Button, Form, FormGroup, Label, Input, ListGroupItem, ListGroup, Row } from 'reactstrap';
const axios = require("axios")

function App() {
  const [cities, setcities] = useState([])
  const [selection, setselection] = useState([])
  
  var selectedCity = "ABSECON"
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

  const updateSelection = (city) =>{
    selectedCity = city.target.value;
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
    console.log(phoneNumber)
    console.log(selection)

    axios.post(`/newnumber`,{
      phone: phoneNumber,
      cities: selection
    })
  }

  return (
    <div className="App">
      <Row>
      <select onChange={updateSelection}>
        {
          cities.map((city) =>
            <option key={city}>{city}</option>
          )
        }
      </select>
      <Button onClick={()=>{
        if(!selection.includes(selectedCity))
          setselection([...selection,selectedCity])}
        } color="primary">Add</Button>{' '}
      </Row>

      <ListGroup style={{alignItems:'center'}}>
      {
        selection.map((number) =>
            <Row>
            <ListGroupItem key={number}>{number}</ListGroupItem>
            <Button outline onClick={()=>removeSelection(number)}color="danger">X</Button>
            </Row>
        )
      }
      </ListGroup>
      
      <Form inline onSubmit={addToDatabase}>
        <FormGroup className="mb-2 mr-sm-2 mb-sm-0">
          <Label for="number" className="mr-sm-2">Phone Number</Label>
          <Input onChange={updatePhone} type="tel" name="number" id="number" placeholder="" />
        </FormGroup>
        <Button>Submit</Button>
      </Form>
    </div>
  );
}

export default App;
