import { DataGrid, GridRowsProp, GridColDef } from "@mui/x-data-grid";
import { FC, useEffect, useState } from "react";
import { getWordsCall } from "../../api";

const columns: GridColDef[] = [
  { field: "title", headerName: "Слово", width: 150 },
  { field: "information", headerName: "Информация", width: 500 },
];

interface IProps {
  text: string;
}

export const Table: FC<IProps> = ({ text }) => {
  const [rows, setRows] = useState<GridRowsProp>([]);

  useEffect(() => {
    if (!text) {
      return;
    }

    const fetchData = async () => {
      try {
        const response = await getWordsCall({ text });

        const newRows: GridRowsProp = Object.keys(response).map((key, idx) => ({
          id: idx,
          title: key,
          information: `Частота: ${response[key].frequency}, Доп. информация: ${response[key].additional_information}`,
        }));

        setRows(newRows);
      } catch (err) {
        console.error(err);
      }
    };

    fetchData();
  }, [text]);

  return (
    <div style={{ height: 700, width: "100%" }}>
      <DataGrid rows={rows} columns={columns} />
    </div>
  );
};
