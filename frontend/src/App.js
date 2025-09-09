import './App.css';
import { useState } from "react";

function App() {
  const [htmlContent, setHtmlContent] = useState(""); 
  const [data, setData] = useState(null); 
  const [loading, setLoading] = useState(false); 
  const [error, setError] = useState(null); 


  const handleSubmit = async () => {
    setLoading(true);
    setError(null);

    // This inserts the user input into a preview div for markup
    const textarea = document.getElementById('textbox');
    const preview = document.getElementById('preview');
    const text = textarea.value;
    preview.innerText = text;


    try {
      const response = await fetch("http://127.0.0.1:5000/analyze-html", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ html: htmlContent }),
        // mode: 'no-cors' 
      });

      if (!response.ok) {
        throw new Error("Failed to analyze HTML");
      }

      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header>
        <h1>ADA Compliance Checker</h1>
      </header>

      <div className="Container">
        <textarea 
          id="textbox" 
          placeholder="Enter HTML here..." 
          value={htmlContent}
          onChange={(e) => setHtmlContent(e.target.value)}
        />
        <div id="preview" className="Card">Submit to see results</div>
        <div className="Container">
          {loading && <p>Loading...</p>}
          {error && <p style={{ color: "red" }}>{error}</p>}
          {data && <Results data={data} />}
        </div>
      </div>

      <div className="Container">
        <button onClick={handleSubmit}>Submit</button>
      </div>

    </div>
  );
}

function Results({ data }) {
  return (
    <div className="Container" id="results">
        <>
          <ul>
            {data.map((error)=><ErrorCard error={error}/>)}
          </ul>
        </>
    </div>
  );
}

function ErrorCard(props) {
  const errorTitles = {
    DOC_LANG_MISSING: "Missing Language Attribute",
    DOC_TITLE_MISSING: "Missing Document Title",
    COLOR_CONTRAST: "Low Contrast Ratio",
    IMG_ALT_MISSING: "Alternative Text",
    IMG_ALT_LENGTH: "Alternative Text Length",
    LINK_GENERIC_TEXT: "Meaningful Link Text",
    HEADING_ORDER: "Hierarchical Order",
    HEADING_MULTIPLE_H1: "Single <h1>"
  };

  const title = errorTitles[props.error.name]

  function resetPreview() {
    const textarea = document.getElementById('textbox');
    const originalPreview = textarea.value;
    const preview = document.getElementById("preview");
    preview.innerText = originalPreview;
  } 

  const handleClick = () => {  
    resetPreview()
    const preview = document.getElementById("preview")  
    const previewText = preview.innerText
    const parser = new DOMParser();
    const doc = parser.parseFromString(previewText, "text/html");

    // Find the target element
    const selector = props.error.selector
    const target = doc.querySelector(selector);
    if (!target) {
        return [previewText, "", ""];
    }
    

    // Get the full HTML of target
    const targetHTML = target.outerHTML;

    //Splits
    var beforeHTML = previewText.split(targetHTML)[0];
    var afterHTML = previewText.split(targetHTML).slice(1).join(targetHTML);


    //Angel -- this is just filler to fix a bug momentarily-- I know this isn't the right solution, just a bandaid
    if (props.error.name === "DOC_LANG_MISSING")
      beforeHTML = ""  
    
    preview.innerHTML = "";

    //Setup divs for preview with highlight
    const beforeDiv = document.createElement("div");
    beforeDiv.innerText = beforeHTML;

    const targetDiv = document.createElement("mark");
    targetDiv.innerText = targetHTML;

    const afterDiv = document.createElement("div");
    afterDiv.innerText = afterHTML;

    preview.appendChild(beforeDiv);
    preview.appendChild(targetDiv);
    preview.appendChild(afterDiv);
  }

   return (
    <div className="Card" onClick={handleClick}>
      <h3>{title}</h3>
      <ul>
        <li><strong>Element:</strong> {props.error.element}</li>
        <li><strong>Details:</strong> {props.error.message}</li>
        <li><strong>Rule:</strong> {props.error.name}</li>
       </ul>
    </div>   
   )
}


export default App;
