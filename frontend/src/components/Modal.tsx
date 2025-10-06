import { Modal as MuiModal, Box, Typography, Button } from "@mui/material";

type ModalProps = {
  open: boolean;
  onClose: () => void;
  title: string;
  message: string;
  type?: 'error' | 'success' | 'info' | 'confirm';
  onConfirm?: () => void;
};

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  boxShadow: 24,
  p: 4,
  borderRadius: 2,
};

const Modal = ({ open, onClose, title, message, type = 'info', onConfirm }: ModalProps) => {
  const getColor = () => {
    switch(type) {
      case 'error': return 'error.main';
      case 'success': return 'success.main';
      case 'confirm': return 'warning.main';
      default: return 'primary.main';
    }
  };

  return (
    <MuiModal
      open={open}
      onClose={onClose}
      aria-labelledby="modal-title"
      aria-describedby="modal-description"
    >
      <Box sx={style}>
        <Typography
          id="modal-title"
          variant="h6"
          component="h2"
          sx={{ color: getColor() }}
        >
          {title}
        </Typography>
        <Typography id="modal-description" sx={{ mt: 2 }}>
          {message}
        </Typography>

        <Box sx={{ mt: 3, display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
          {type === 'confirm' && onConfirm && (
            <>
              <Button onClick={onClose} variant="outlined">
                キャンセル
              </Button>
              <Button onClick={onConfirm} variant="contained" color="primary">
                確認
              </Button>
            </>
          )}
          {type !== 'confirm' && (
            <Button onClick={onClose} variant="contained">
              閉じる
            </Button>
          )}
        </Box>
      </Box>
    </MuiModal>
  );
};

export default Modal;
