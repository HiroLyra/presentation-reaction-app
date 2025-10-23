import { Container, Box, Typography, Button, Paper, Grid } from "@mui/material";
import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { QRCodeSVG } from "qrcode.react";
import { getPresentation, addReaction } from "../api/presentationApi";
import type { GetPresentationResponse } from "../types/presentation";
import Modal from "../components/Modal";
import { useWebSocket } from "../hooks/useWebSocket";

const PresentationPage = () => {
  const { id } = useParams<{ id: string }>();
  const [presentation, setPresentation] =
    useState<GetPresentationResponse | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [modalTitle, setModalTitle] = useState("");
  const [modalMessage, setModalMessage] = useState("");
  const [modalType, setModalType] = useState<
    "error" | "success" | "info" | "confirm"
  >("info");

  const presentationId = id || "";

  const { sendMessage } = useWebSocket({
    url: `wss://presentation-reaction-api.onrender.com/ws/presentations/${presentationId}/`,
    onMessage: (data) => {
      fetchPresentation();
    },
  });

  const fetchPresentation = async () => {
    try {
      const data = await getPresentation(presentationId);
      setPresentation(data);
    } catch (error) {
      console.error("エラー:", error);
      setModalTitle("エラー");
      setModalMessage("発表情報の取得に失敗しました");
      setModalType("error");
      setModalOpen(true);
    }
  };

  useEffect(() => {
    fetchPresentation();
  }, [presentationId]);

  const handleReaction = (
    reactionType: "thumbs_up" | "heart" | "laugh" | "surprise"
  ) => {
    try {
      sendMessage({ reaction_type: reactionType });
    } catch (error) {
      console.error("エラー:", error);
      setModalTitle("エラー");
      setModalMessage("反応の送信に失敗しました");
      setModalType("error");
      setModalOpen(true);
    }
  };

  if (!presentation) {
    return (
      <Container maxWidth="md">
        <Box sx={{ mt: 4, textAlign: "center" }}>
          <Typography>読み込み中...</Typography>
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth={false} sx={{ px: 4 }}>
      <Box sx={{ mt: 4, mb: 4 }}>
        <Paper sx={{ p: 4, mb: 4 }}>
          <Typography
            variant="h2"
            component="h1"
            gutterBottom
            sx={{ fontWeight: "bold", textAlign: "center" }}
          >
            {presentation.title}
          </Typography>

          {presentation.description && (
            <Typography
              variant="body1"
              sx={{ textAlign: "center", color: "text.secondary", mb: 2 }}
            >
              {presentation.description}
            </Typography>
          )}

          <Box sx={{ mt: 4 }}>
            <Grid container spacing={3} justifyContent="center">
              <Grid size={{ xs: 6, sm: 3, md: 2 }}>
                <Box sx={{ textAlign: "center" }}>
                  <Typography variant="h1" sx={{ fontSize: "4rem" }}>
                    👍
                  </Typography>
                  <Typography variant="h3" sx={{ fontWeight: "bold" }}>
                    {presentation.thumbs_up}
                  </Typography>
                </Box>
              </Grid>
              <Grid size={{ xs: 6, sm: 3, md: 2 }}>
                <Box sx={{ textAlign: "center" }}>
                  <Typography variant="h1" sx={{ fontSize: "4rem" }}>
                    ❤️
                  </Typography>
                  <Typography variant="h3" sx={{ fontWeight: "bold" }}>
                    {presentation.heart}
                  </Typography>
                </Box>
              </Grid>
              <Grid size={{ xs: 6, sm: 3, md: 2 }}>
                <Box sx={{ textAlign: "center" }}>
                  <Typography variant="h1" sx={{ fontSize: "4rem" }}>
                    😂
                  </Typography>
                  <Typography variant="h3" sx={{ fontWeight: "bold" }}>
                    {presentation.laugh}
                  </Typography>
                </Box>
              </Grid>
              <Grid size={{ xs: 6, sm: 3, md: 2 }}>
                <Box sx={{ textAlign: "center" }}>
                  <Typography variant="h1" sx={{ fontSize: "4rem" }}>
                    😮
                  </Typography>
                  <Typography variant="h3" sx={{ fontWeight: "bold" }}>
                    {presentation.surprise}
                  </Typography>
                </Box>
              </Grid>
            </Grid>
          </Box>
        </Paper>

        <Grid container spacing={4}>
          <Grid size={{ xs: 12, md: 6 }}>
            <Paper sx={{ p: 2 }}>
              <Box
                sx={{
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                  flexDirection: "column",
                }}
              >
                <Box sx={{ p: 1.5, bgcolor: "white", borderRadius: 2 }}>
                  <QRCodeSVG
                    value={window.location.href}
                    size={180}
                    level="H"
                  />
                </Box>
              </Box>
            </Paper>
          </Grid>

          <Grid size={{ xs: 12, md: 6 }}>
            <Paper sx={{ p: 2 }}>
              <Grid container spacing={2}>
                <Grid size={{ xs: 6 }}>
                  <Button
                    variant="contained"
                    fullWidth
                    sx={{ fontSize: "3rem", py: 2, height: "100px" }}
                    onClick={() => handleReaction("thumbs_up")}
                  >
                    👍
                  </Button>
                </Grid>
                <Grid size={{ xs: 6 }}>
                  <Button
                    variant="contained"
                    fullWidth
                    sx={{ fontSize: "3rem", py: 2, height: "100px" }}
                    onClick={() => handleReaction("heart")}
                  >
                    ❤️
                  </Button>
                </Grid>
                <Grid size={{ xs: 6 }}>
                  <Button
                    variant="contained"
                    fullWidth
                    sx={{ fontSize: "3rem", py: 2, height: "100px" }}
                    onClick={() => handleReaction("laugh")}
                  >
                    😂
                  </Button>
                </Grid>
                <Grid size={{ xs: 6 }}>
                  <Button
                    variant="contained"
                    fullWidth
                    sx={{ fontSize: "3rem", py: 2, height: "100px" }}
                    onClick={() => handleReaction("surprise")}
                  >
                    😮
                  </Button>
                </Grid>
              </Grid>
            </Paper>
          </Grid>
        </Grid>
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

export default PresentationPage;
