<template>
  <div class="loading">
    <img
        src="../assets/loading.svg"
        alt="拼命加载中..."
    >
  </div>
</template>
<script lang="ts">
import {defineComponent} from "vue";

export default defineComponent({
  name: "CustomLoading",
});
</script>
<style scoped>
.loading {
  text-align: center;
  padding: 30px;
}
</style>
