import toast from "react-hot-toast";

const notify = {

    success(message) {
        toast.success(message);
    },

    error(message) {
        toast.error(message);
    },

    loading(message) {
        return toast.loading(message);
    },

    dismiss(id) {
        toast.dismiss(id);
    },

    info(message) {
        toast(message);
    }

};

export default notify;
