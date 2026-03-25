

myPizzaPromise
  .then(data => console.log(data))   // Runs if resolved
  .catch(err => console.error(err)); // Runs if rejected