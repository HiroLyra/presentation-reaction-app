import { Container, TextField, Button, Box, Typography } from "@mui/material";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createPresentation } from "../api/presentationApi";
import Modal from "../components/Modal";

const CreatePresentationPage = () => {
  const navigate = useNavigate();
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [modalOpen, setModalOpen] = useState(false);
  const [modalTitle, setModalTitle] = useState("");
  const [modalMessage, setModalMessage] = useState("");
  const [modalType, setModalType] = useState<
    "error" | "success" | "info" | "confirm"
  >("info");

  const handleSubmit = async () => {
    if (!title) {
      setModalTitle("");
      setModalMessage("タイトルを入力してください");
      setModalType("info");
      setModalOpen(true);
      return;
    }
    try {
      const response = await createPresentation({ title, description });
      console.log("成功:", response);
      navigate(`/presentation/${response.id}`);
    } catch (error) {
      console.error("エラー:", error);
      setModalTitle("エラー");
      setModalMessage("発表の作成に失敗しました");
      setModalType("error");
      setModalOpen(true);
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

      <Modal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        title={modalTitle}
        message={modalMessage}
        type={modalType}
      />
    </Container>
  );
};

export default CreatePresentationPage;
