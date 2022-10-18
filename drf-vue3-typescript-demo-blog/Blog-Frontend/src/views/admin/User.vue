<template>
  <div>
    <div>
      <el-form :inline="true" :model="state.params" class="demo-form-inline">
        <el-form-item label="名称">
          <el-input v-model="state.params.name" placeholder="账号"/>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="state.params.is_active" placeholder="请选择">
            <el-option :value="1" label="生效"/>
            <el-option :value="0" label="禁用"/>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button :loading="state.isLoading" type="primary" @click="handleSearch">查询</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div>
      <el-table ref="userTable" :data="state.userList" :header-cell-style="{background:'#eef1f6',color:'#606266'}"
                stripe>
        <el-table-column type="selection" width="55"/>
        <el-table-column label="ID" prop="id" width="80"/>
        <el-table-column label="账号" prop="username" width="200"/>
        <el-table-column label="昵称" prop="nickname" width="200"/>
        <el-table-column label="状态" prop="is_active"/>
        <el-table-column :formatter="datetimeFormatter" label="注册时间" prop="created_at"/>
        <el-table-column label="操作">
          <template #default="scope">
            <el-popconfirm v-if="scope.row.is_active" cancelButtonText='取消' confirmButtonText='禁用' icon="el-icon-info"
                           iconColor="red" title="确定禁用该用户吗？" @confirm="disableUser(scope.$index,scope.row)">
              <template #reference>
                <el-button size="small" type="text">
                  禁用
                </el-button>
              </template>
            </el-popconfirm>
            <el-button v-if="!scope.row.is_active" size="small" type="text"
                       @click.prevent="enableUser(scope.$index, scope.row)">
              启用
            </el-button>
            <el-button size="small" type="text"
                       @click.prevent="showUserDetail(scope.row)">
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
  <UserDetail
      :user-id="state.userId"
      :visible="state.showDialog"
      @close="state.showDialog = false"
  />
</template>

<script lang="ts">
import {defineComponent, reactive} from "vue";
import {ResponseData, User} from "../../types";
import {ElMessage} from "element-plus";
import {timestampToTime} from "../../utils";
import {getUserList, saveUser} from "../../api/service";
import UserDetail from "../../components/UserDetail.vue";

export default defineComponent({
  name: "User",
  components: {UserDetail},
  setup: function () {
    const state = reactive({
      userList: [] as Array<User>,
      params: {
        name: '',
        role: 'Reader',
        is_active: undefined,
        page: 1,
        page_size: 10,
      },
      isLoading: false,
      total: 0,
      showDialog: false,
      userId: 0,
      saveLoading: false,
    });

    const handleSearch = async (): Promise<void> => {
      state.isLoading = true;
      try {
        const data: ResponseData = await getUserList(state.params);
        state.isLoading = false;
        state.userList = data.results;
        state.total = data.count
      } catch (e) {
        console.error(e)
        state.isLoading = false;
      }
    };

    const disableUser = async (index: number, row: User) => {
      await saveUser('patch', {id: row.id, is_active: false} as User);
      ElMessage({
        message: "禁用成功！",
        type: "success",
      });
      await handleSearch()
    }

    const enableUser = async (index: number, row: User) => {
      await saveUser('patch', {id: row.id, is_active: true} as User);
      ElMessage({
        message: "启用成功！",
        type: "success",
      });
      await handleSearch()
    }

    const datetimeFormatter = (row: User, column: number, cellValue: string, index: number) => {
      return timestampToTime(cellValue, true);
    }

    handleSearch()
    return {
      state,
      handleSearch,
      datetimeFormatter,
      disableUser,
      enableUser,
    }
  },
  methods: {
    showUserDetail(row: User) {
      this.state.userId = row.id
      this.state.showDialog = true;
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