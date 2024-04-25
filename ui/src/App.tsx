import { Table } from "./components/Table";
import { InputBar } from "./components/Input";
import { useState } from "react";

function App() {
  const [text, setText] = useState<string>("");

  const handleChangeText = (newText: string) => {
    setText(newText);
  };

  return (
    <>
      <InputBar onInputChange={handleChangeText} />
      <Table text={text} />
    </>
  );
}

export default App;
