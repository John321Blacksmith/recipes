import React, { Component } from 'react';
import axios from 'axios';


const recipes = [
    {
        "id": 2,
        "title": "admin's recipe",
        "date": "2023-06-22T19:17:02.014605Z",
        "ingredients": "test admin",
        "category": "cat admin",
        "instruction": "ADMIN",
        "author": 1
    },
    {
        "id": 4,
        "title": "Mike's recipe",
        "date": "2023-06-23T09:30:10.521571Z",
        "ingredients": "Mike's ingredients",
        "category": "brother's kitchen",
        "instruction": "how Mike cooks dishes",
        "author": 4
    },
    {
        "id": 5,
        "title": "Jack's recipe",
        "date": "2023-06-23T09:31:22.130847Z",
        "ingredients": "Jack's ingredients",
        "category": "friend's kitchen",
        "instruction": "How Jack cooks dishes",
        "author": 5
    },
    {
        "id": 6,
        "title": "Mike's recipe",
        "date": "2023-06-24T15:39:45.488172Z",
        "ingredients": "Mike's ingredients",
        "category": "brother's kitchen",
        "instruction": "how Mike cooks dishes and many more",
        "author": 4
    },
    {
        "id": 7,
        "title": "Mike's recipe",
        "date": "2023-06-24T16:18:13.219162Z",
        "ingredients": "Mike's ingredients",
        "category": "brother's kitchen",
        "instruction": "how Mike cooks dishes(edited)",
        "author": 4
    },
    {
        "id": 8,
        "title": "Jack's recipe",
        "date": "2023-06-24T16:25:48.994790Z",
        "ingredients": "Jack's ingredients",
        "category": "friend's kitchen",
        "instruction": "How Jack cooks dishes and deserts",
        "author": 5
    }
]

// class App extends Component {
//   state = {
//     recipes: []
//   };

//   componentDidMount() {
//     this.getRecipes();
//   }

//   // fill up the recipes collection
//   // objects from backend
//   getRecipes() {
//     axios
//     .get('/api/v1/recipes/')
//     .then(res => {
//       this.setState({ recipes: res.data });
//     })
//     .catch(err => {
//       console.log(err);
//     });
//   }

//   render() {
//     return (
//       <div>
//       {this.state.recipes.map(item => (
//           <div key={item.id}>
//             <p>Title: {item.title}</p>
//             <p>Date: {item.date}</p>
//             <p>Author: {item.author}</p>
//             <p>Category: {item.category}</p>
//             <p>Ingredients: {item.ingredients}</p>
//             <p>instruction: {item.instruction}</p>
//             <br/>
//             <br/>
//             <br/>
//             <br/>
//           </div>
//         ))}
//     </div>
//     );
//   }
// }

// export default App;


class App extends Component() {
  constructor(props) {
    super(props);
    this.state = { recipes };
  };

  render()

}