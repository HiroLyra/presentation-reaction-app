import { Container, TextField, Button, Box, Typography } from "@mui/material";
import { useState } from "react";
import { createPresentation } from "../api/presentationApi";

const CreatePresentationPage = () => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const handleSubmit = async () => {
    if (!title) {
      alert("タイトルを入力してください");
      return;
    }
    try {
      const response = await createPresentation({ title, description });
      console.log("成功:", response);
    } catch (error) {
      console.error("エラー:", error);
      alert("発表の作成に失敗しました");
    }
  };
  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          発表作成
        </Typography>

        <TextField
          label="タイトル"
          variant="outlined"
          fullWidth
          margin="normal"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />

        <TextField
          label="説明"
          variant="outlined"
          fullWidth
          multiline
          rows={4}
          margin="normal"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />

        <Button
          variant="contained"
          color="primary"
          fullWidth
          sx={{ mt: 2 }}
          onClick={handleSubmit}
        >
          作成
        </Button>
      </Box>
    </Container>
  );
};

export default CreatePresentationPage;
