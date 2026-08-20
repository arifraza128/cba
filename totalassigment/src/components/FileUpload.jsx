import { useRef, useState } from 'react';

function FileUpload() {
  const fileInput = useRef(null);
  const [fileName, setFileName] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();

    const file = fileInput.current.files[0];

    if (file) {
      setFileName(file.name);
    }
  };

  return (
    <div>
      <h2>File Upload</h2>

      <form onSubmit={handleSubmit} className="upload-box">
        <input type="file" ref={fileInput} />
        <button type="submit">Upload</button>
      </form>

      {fileName && <p>Selected File: {fileName}</p>}
    </div>
  );
}

export default FileUpload;
