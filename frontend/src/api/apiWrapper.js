import axios from 'axios';


const TOKEN = "a793c98cbb4fb3c63c9053439168683d";
const API_URL = `http://2.59.42.47:8000/api/v1/{}`;


String.prototype.format = function () {
    let i = 0, args = arguments;
    return this.replace(/{}/g, function () {
        return typeof args[i] != 'undefined' ? args[i++] : '';
    });
};


export const apiWrapper = async query => {
    const response = await axios.get(API_URL.format(query), {
        params: {
            api_token: TOKEN
        }
    });
    return response;
}