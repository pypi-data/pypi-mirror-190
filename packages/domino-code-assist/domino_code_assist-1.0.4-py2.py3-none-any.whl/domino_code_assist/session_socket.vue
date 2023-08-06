<script>
  module.exports = {
    created() {
      if (!window.sessionSockets) {
        window.sessionSockets = {};
      }
      const current = window.sessionSockets[this.notebookId];

    }
  }
</script>