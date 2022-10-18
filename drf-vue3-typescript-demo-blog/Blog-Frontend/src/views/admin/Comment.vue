<template>
  <div>
    <div>
      <el-form :inline="true" :model="state.params" class="demo-form-inline">
        <el-form-item label="账号">
          <el-select v-model="state.params.user" filterable placeholder="请选择">
            <el-option
                v-for="item in state.userList"
                :key="item.id"
                :label="item.nickname || item.username"
                :value="item.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="内容">
          <el-input v-model="state.params.content" placeholder="评论内容"/>
        </el-form-item>
        <el-form-item>
          <el-button :loading="state.loading" type="primary" @click="handleSearch">查询</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div>
      <el-table ref="articleTable" :data="state.commentList" :header-cell-style="{background:'#eef1f6',color:'#606266'}"
                stripe>
        <el-table-column type="selection" width="55"/>
        <el-table-column label="ID" prop="id" width="80"/>
        <el-table-column label="评论者" prop="user_info.name" width="200"/>
        <el-table-column label="评论内容" prop="content" width="200"/>
        <el-table-column label="文章" prop="article_info.title"/>
        <el-table-column label="回复评论" prop="reply.id" width="200"/>
        <el-table-column :formatter="datetimeFormatter" label="评论时间" prop="created_at"/>
        <el-table-column label="操作">
          <template #default="scope">
            <el-button size="small" type="text"
                       @click.prevent="showDetail(scope.row)">
              详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div class="pagination">
      <el-pagination :page-size="10" :total="state.total" background
                     layout="prev, pager, next"></el-pagination>
    </div>
  </div>
</template>

<script lang="ts">
import {defineComponent, reactive} from "vue";
import {Article, CommentInfo, CommentPara, ResponseData, User} from "../../types";
import {ElMessage} from "element-plus";
import {timestampToTime} from "../../utils";
import {getCommentList, getUserList, saveUser} from "../../api/service";
import UserDetail from "../../components/UserDetail.vue";

export default defineComponent({
  name: "Comment",
  components: {UserDetail},
  setup: function () {
    const state = reactive({
      commentList: [] as Array<CommentInfo>,
      params: {
        user: undefined,
        article: undefined,
        reply: undefined,
        content: '',
        page: 1,
        page_size: 10,
      } as unknown as CommentPara,
      total: 0,
      userList: [] as Array<User>,
      loading: false,
    });

    const handleSearch = async (): Promise<void> => {
      state.loading = true;
      try {
        const data: ResponseData = await getCommentList(state.params);
        state.loading = false;
        state.commentList = data.results;
        state.total = data.count
      } catch (e) {
        console.error(e)
        state.loading = false;
      }
    };

    const getUsers = async (): Promise<void> => {
      try {
        const data: ResponseData = await getUserList({});
        state.userList = data.results;
      } catch (e) {
        console.error(e)
      }
    };


    const datetimeFormatter = (row: Article, column: number, cellValue: string, index: number) => {
      return timestampToTime(cellValue, true);
    }

    handleSearch()
    getUsers()
    return {
      state,
      handleSearch,
      datetimeFormatter,
    }
  },
  methods: {
    showDetail(row: CommentInfo) {
      const {href} = this.$router.resolve({
        path: '/article/',
        query: {
          id: row.article_info.id
        }
      });
      window.open(href, "_blank");
    },
  }
})
</script>

<style scoped>
.pagination {
  text-align: right;
  margin-top: 12px;
}
</style>