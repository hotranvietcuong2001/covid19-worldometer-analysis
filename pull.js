import fetch from 'node-fetch'

async function foo() {
    const res = await fetch('https://restcountries.com/v2/all');
    console.log(res);

    return res
}

console.log(foo())