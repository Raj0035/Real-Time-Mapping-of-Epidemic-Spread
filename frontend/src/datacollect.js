import axios from 'axios';

const fetchData = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5001/data');
    return response.data;
  } catch (error) {
    console.error('Error fetching data:', error);
    return [];
  }
};
console.log("accessed")
export default fetchData;
