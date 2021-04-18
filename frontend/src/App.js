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
    update();
  }, [])

  async function update(){
    axios.get("https://www.cvs.com/immunizations/covid-19-vaccine/immunizations/covid-19-vaccine.vaccine-status.NJ.json?vaccineinfo",{
    }).then(res => {
      let x = res.data['responsePayloadData']['data']['NJ'];
      console.log(x.length)
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

  const removeSelection = (city) =>{
    const index = selection.indexOf(city.target.innerText);
    var x = selection
    x.splice(index,1)
    console.log(x)
    setselection(x)
  }

  const updatePhone = (phone) =>{
    phoneNumber = phone.target.value;
  }

  const addToDatabase = (number) =>{
    console.log(phoneNumber)
    console.log()
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

      <ListGroup>
        {
          selection.map((number) =>
            <ListGroupItem onClick={removeSelection} key={number}>{number}</ListGroupItem>
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
