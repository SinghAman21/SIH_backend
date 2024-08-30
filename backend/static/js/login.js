let slide2=document.getElementById("slide2");
let slide1=document.getElementById("slide1");
let slide3=document.getElementById("slide3");
let btn1=document.getElementById("s1");
let btn2=document.getElementById("s2");
let btn3=document.getElementById("s3");
slide2.classList.add('hidden');
// slide1.classList.add('hidden');
slide3.classList.add('hidden');
// btn1.classList.add('btnhid');
btn2.classList.add('btnhid');
btn3.classList.add('btnhid');
let changeto2=() =>{
    slide2.classList.remove('hidden'),
    slide1.classList.add('hidden'),
    slide3.classList.add('hidden'),
    btn2.classList.remove('btnhid'),
    btn1.classList.add('btnhid'),
    btn3.classList.add('btnhid')
}
let changeto1=() =>{
    slide1.classList.remove('hidden'),
    slide2.classList.add('hidden'),
    slide3.classList.add('hidden'),
    btn1.classList.remove('btnhid'),
    btn2.classList.add('btnhid'),
    btn3.classList.add('btnhid')
}
let changeto3=() =>{
    slide3.classList.remove('hidden'),
    slide1.classList.add('hidden'),
    slide2.classList.add('hidden'),
    btn3.classList.remove('btnhid'),
    btn1.classList.add('btnhid'),
    btn2.classList.add('btnhid')
}
btn2.addEventListener("click", changeto2)
btn1.addEventListener("click", changeto1)
btn3.addEventListener("click", changeto3)