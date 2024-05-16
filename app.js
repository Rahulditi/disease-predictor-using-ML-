const express = require('express');
const bodyParser = require('body-parser');
const path = require('path')
const {PythonShell} = require('python-shell')

const app = express();
const port = 3000;

app.set('view engine','ejs')

app.use(express.static('public'))
app.use(bodyParser.json())
app.use('/css',express.static(__dirname + 'public/css'))
app.use('/js',express.static(__dirname + 'public/js'))
app.use('/img',express.static(__dirname + 'public/img'))
app.use(bodyParser.urlencoded({ extended: true }))


app.get('',(req,res)=>{
    res.render('index',{result:"a"})
})
app.post('/submit', async(req, res) => {
    
    const selectedItems = req.body.items;
    let ans = await sendfile(selectedItems)
    const resultData = {processedData:ans};
    res.json(resultData);

});


const sendfile = async(data) =>{
    let result = ""
    let options = {
        mode:"json",
        args: JSON.stringify(data),
        pythonPath: 'python'
    }
    try{
        result = await PythonShell.run(path.join(__dirname, 'prediction.py'), options)

    }
    catch(err){
        console.log(err);
    }
    console.log(result[0][0]);
    return result
}

app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});
