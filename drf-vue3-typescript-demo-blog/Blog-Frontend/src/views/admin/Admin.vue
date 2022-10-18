<template>
  <div class="body">
    <div class="menu">
      <el-menu :default-active="state.activePath" :router="true">
        <el-menu-item index="AdminDashboard" route="/admin/dashboard"><i class="el-icon-s-home"></i> Dashboard
        </el-menu-item>
        <el-menu-item index="ArticleManagement" route="/admin/article"><i class="el-icon-s-order"></i> 文章
        </el-menu-item>
        <el-menu-item index="TagManagement" route="/admin/tag"><i class="el-icon-collection-tag"></i> 标签</el-menu-item>
        <el-menu-item index="CommentManagement" route="/admin/comment"><i class="el-icon-chat-line-round"></i> 评论
        </el-menu-item>
        <el-menu-item index="UserManagement" route="/admin/user"><i class="el-icon-user"></i> 用户</el-menu-item>
      </el-menu>
    </div>
    <div class="view">
      <router-view/>
    </div>
  </div>
</template>

<script>
import {defineComponent, reactive} from "vue";
import {useRoute} from "vue-router";

export default defineComponent({
  name: "Admin",
  setup() {
    const state = reactive({
      activePath: '',
    });
    const route = useRoute()
    if (route.name === 'Dashboard') {
      state.activePath = 'AdminDashboard'
    } else {
      state.activePath = route.name;
    }
    return {
      state,
    }
  },
});
</script>


<style lang="less" scoped>
.body {
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  display: flex;
}

.user {
  font-size: 20px;
}

.menu {
  width: 200px;
}

.view {
  width: calc(100% - 200px);
  padding: 24px;
}

.el-menu {
  height: 100%;
}

</style>