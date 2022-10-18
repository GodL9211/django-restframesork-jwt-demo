<template>
  <div>
    <div>
      <el-form :inline="true" :model="state.params" class="demo-form-inline">
        <el-form-item label="名称">
          <el-input v-model="state.params.name" placeholder="名称" />
        </el-form-item>
        <el-form-item>
          <el-button
            :loading="state.isLoading"
            type="primary"
            @click="handleSearch"
            >查询</el-button
          >
        </el-form-item>
      </el-form>
    </div>
    <div class="button-container">
      <el-button
        :loading="state.isLoading"
        type="primary"
        @click="showAddDialog"
        ><i class="el-icon-plus" /> 新 增
      </el-button>
    </div>
    <div>
      <el-table
        ref="tagTable"
        :data="state.tagList"
        :header-cell-style="{ background: '#eef1f6', color: '#606266' }"
        stripe
      >
        <el-table-column type="selection" width="55" />
        <el-table-column label="ID" prop="id" width="80" />
        <el-table-column label="名称" prop="name" width="200" />
        <el-table-column
          :formatter="datetimeFormatter"
          label="修改时间"
          prop="modified_at"
        />
        <el-table-column fixed="right" label="操作" width="120">
          <template #default="scope">
            <el-popconfirm
              cancelButtonText="取消"
              confirmButtonText="删除"
              icon="el-icon-info"
              iconColor="red"
              title="确定删除系列吗？"
              @confirm="deleteObject(scope.$index, scope.row)"
            >
              <template #reference>
                <el-button size="small" type="text"> 删除 </el-button>
              </template>
            </el-popconfirm>
            <el-button
              size="small"
              type="text"
              @click.prevent="showEditDialog(scope.$index, scope.row)"
            >
              编辑
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div class="pagination">
      <el-pagination
        :page-size="10"
        :total="state.total"
        background
        layout="prev, pager, next"
      ></el-pagination>
    </div>
  </div>
  <TagEditDialog
    :loading="state.saveLoading"
    :tag="state.tag"
    :visible="state.showDialog"
    @close="handleCloseDialog"
  />
</template>

<script lang="ts">
import { defineComponent, reactive } from "vue";
import { ResponseData, Tag } from "../../types";
import { addTag, deleteTag, getTagList, saveTag } from "../../api/service";
import { timestampToTime } from "../../utils";
import { ElMessage } from "element-plus";
import TagEditDialog from "../../components/TagEditDialog.vue";
import { useRoute } from "vue-router";

export default defineComponent({
  name: "Tag",
  components: { TagEditDialog },
  watch: {
    "$route.path": {
      handler(val, oldVal) {
        if (val !== oldVal && ["/admin/tag"].includes(val)) this.handleSearch();
      },
      deep: true,
    },
  },
  setup: function () {
    const route = useRoute();
    const state = reactive({
      tagList: [] as Array<Tag>,
      params: {
        name: undefined,
        page: 1,
        page_size: 10,
      },
      isLoading: false,
      total: 0,
      showDialog: false,
      tag: {
        id: 0,
        name: "",
      } as Tag,
      saveLoading: false,
    });

    const handleSearch = async (): Promise<void> => {
      state.isLoading = true;
      try {
        const data: ResponseData = await getTagList(state.params);
        state.isLoading = false;
        state.tagList = data.results;
        state.total = data.count;
      } catch (e) {
        console.error(e);
        state.isLoading = false;
      }
    };

    const deleteObject = async (index: number, row: Tag) => {
      await deleteTag(row.id);
      ElMessage({
        message: "删除成功！",
        type: "success",
      });
      await handleSearch();
    };

    const datetimeFormatter = (
      row: Tag,
      column: number,
      cellValue: string,
      index: number
    ) => {
      return timestampToTime(cellValue, true);
    };

    handleSearch();
    return {
      state,
      handleSearch,
      datetimeFormatter,
      deleteObject,
    };
  },
  methods: {
    showEditDialog(index: number, row: Tag) {
      this.state.tag = row;
      this.state.showDialog = true;
    },

    showAddDialog() {
      this.state.tag = {} as Tag;
      this.state.showDialog = true;
    },

    async handleCloseDialog(params: any) {
      if (!params.isOk) {
        this.state.showDialog = false;
        return;
      }
      this.state.saveLoading = true;
      const method = this.state.tag.id ? "put" : "post";
      try {
        await saveTag(method, params.obj);
        this.state.showDialog = false;
        this.state.saveLoading = false;
        await this.handleSearch();
      } catch (e) {
        console.error(e);
        this.state.saveLoading = false;
      }
    },
  },
});
</script>

<style scoped>
.pagination {
  text-align: right;
  margin-top: 12px;
}
</style>