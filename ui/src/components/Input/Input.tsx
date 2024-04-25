import * as React from "react";

import { FC, useState } from "react";

import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import { ListItem, List } from "@mui/material";
import { Input } from '@mui/material';
import Modal from "@mui/material/Modal";
import { getWordsCall } from "../../api";
import {
  GetContextRequest,
  GetContextResponse,
  getContextCall,
} from "../../api/getContext";

interface IProps {
  onInputChange: (newText: string) => void;
}

const style = {
  position: "absolute" as "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 400,
  bgcolor: "background.paper",
  border: "2px solid #000",
  boxShadow: 24,
  p: 4,
};

export const InputBar: FC<IProps> = ({ onInputChange }) => {
  const [query, setQuery] = useState<string>("");

  const [contextRequest, setContextRequest] = useState<GetContextRequest>({
    word: "",
    length: 0,
    count: 0,
  });
  const [contextResponse, setContextResponse] = useState<GetContextResponse>({
    context: "",
  });

  const handleInputChange = (evt: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(evt.target.value);
    onInputChange(evt.target.value);
  };

  const [openHelp, setOpenHelp] = useState(false);
  const handleOpenHelp = () => setOpenHelp(true);
  const handleCloseHelp = () => setOpenHelp(false);

  const [openContext, setOpenContext] = useState(false);
  const handleOpenContext = () => setOpenContext(true);
  const handleCloseContext = () => setOpenContext(false);

  const handleContextRequestChange = (evt) => {
    const { name, value } = evt.target;
    setContextRequest({
      ...contextRequest,
      [name]: value,
    });
  };
  const handleGetContextResponse = async () => {
    try {
      const response = await getContextCall(contextRequest);
      setContextResponse(response);
    } catch (err) {
      console.error(err);
      return;
    }
  };

  const importFile = (evt) => {
      const file = evt.target.files[0];
    if (!file) {
      return;
    }

    const reader = new FileReader();

    reader.onload = (e) => {
      onInputChange(e.target!.result as string);
      setQuery(e.target!.result as string)
    };

    reader.readAsText(file);
};

  const exportResult = async () => {
    try {
      const result = await getWordsCall({ text: query });
      const dataStr =
        "data:text/json;charset=utf-8," +
        encodeURIComponent(JSON.stringify(result));

      const downloadAnchorNode = document.createElement("a");

      downloadAnchorNode.setAttribute("href", dataStr);
      downloadAnchorNode.setAttribute("download", "result.json");

      document.body.appendChild(downloadAnchorNode);

      downloadAnchorNode.click();
      downloadAnchorNode.remove();
    } catch (err) {
      console.error(err);
      return;
    }
  };

  return (
    <Box
      display="flex"
      alignItems="center"
      justifyContent="space-between"
      width="100%"
      p={1}
    >
      <TextField
        variant="outlined"
        label="Поиск"
        fullWidth
        style={{ marginRight: 8 }}
        onChange={handleInputChange}
      />
      <Box display="flex" alignItems="center" justifyContent="space-between">
        <Button
          variant="contained"
          color="primary"
          style={{ marginRight: 4 }}
          onClick={handleOpenContext}
        >
          Контекст
        </Button>
        <Modal open={openContext} onClose={handleCloseContext}>
          <Box sx={style}>
            <Typography variant="h6" component="h2">
              Контекст
            </Typography>
            <TextField
              margin="normal"
              fullWidth
              name="word"
              label="Слово"
              value={contextRequest.word}
              onChange={handleContextRequestChange}
            />
            <TextField
              margin="normal"
              fullWidth
              name="length"
              label="Длина"
              value={contextRequest.length}
              onChange={handleContextRequestChange}
            />
            <TextField
              margin="normal"
              fullWidth
              name="count"
              label="Количество"
              value={contextRequest.count}
              onChange={handleContextRequestChange}
            />
            <Box sx={{ display: "flex", justifyContent: "flex-end", mt: 2 }}>
              <Button
                variant="outlined"
                onClick={handleCloseContext}
                sx={{ mr: 1 }}
              >
                Выйти
              </Button>
              <Button variant="contained" onClick={handleGetContextResponse}>
                Подтвердить
              </Button>
            </Box>
            {contextResponse.context != "" ? (
              <Box
                sx={{
                  maxWidth: "600px",
                  border: "1px solid #ccc",
                  borderRadius: "4px",
                  p: 2,
                }}
              >
                <Typography variant="h6">Результат</Typography>
                <List>
                  {contextResponse["context"].split("\n").map((item, idx) => {
                    return (
                      <ListItem key={idx}>
                        {item.trim()}
                      </ListItem>
                    );
                  })}
                </List>
              </Box>
            ) : (
              <></>
            )}
          </Box>
        </Modal>

        <Button
          variant="contained"
          color="primary"
          style={{ marginRight: 4 }}
          onClick={handleOpenHelp}
        >
          Помощь
        </Button>
        <Modal
          open={openHelp}
          onClose={handleCloseHelp}
          aria-labelledby="modal-modal-title"
          aria-describedby="modal-modal-description"
        >
          <Box sx={style}>
            <Typography id="modal-modal-title" variant="h6" component="h2">
              Помощь
            </Typography>
            <Typography id="modal-modal-description" sx={{ mt: 2 }}>
              <p>
                1. Для импорта текста необходимо нажать на кнопку "Импортировать
                текст", также есть возможность писать текст вручную.
              </p>

              <p>
                2. Для разбора текста необходимо нажать кнопку "Разобрать
                текст", после чего появится таблица с результатом. В данной
                таблице можно редактировать дополнительнею информацию, которая
                представлена в 3 колонке.
              </p>

              <p>
                4. При нажатии на "Очистить", уберется таблица, при поыторном
                нажатии мы удалим весь введенный текст.
              </p>

              <p>
                5. Также есть возможность сохранить текст в файл в формате JSON,
                для комфортной визуализации результатов.
              </p>

              <p>
                6. Кроме того, после разбора текста можно начажать на "Фильрация
                и поиск" для фильтрации и поиска по словам, частоте и
                дополнительной информации. Удачи!
              </p>
            </Typography>
          </Box>
        </Modal>
        <Button
          variant="contained"
          color="primary"
          style={{ marginRight: 6 }}
          onClick={exportResult}
        >
          Экспорт
        </Button>
        <Input
          type="file"
          variant="contained"
          color="primary"
          style={{ marginRight: 6 }}
          onChange={importFile}
        >
            Импорт
        </Input>

      </Box>
    </Box>
  );
};
