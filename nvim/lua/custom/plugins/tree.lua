vim.cmd([[ let g:neo_tree_remove_legacy_commands = 1 ]])

return {
  "nvim-neo-tree/neo-tree.nvim",
  version = "*",
  dependencies = {
    "nvim-lua/plenary.nvim",
    "nvim-tree/nvim-web-devicons", -- not strictly required, but recommended
    "MunifTanjim/nui.nvim",
  },
  config = function()
    vim.keymap.set('n', '<leader>t', ':Neotree toggle<cr>', { desc = "Toggle [T]ree" })

    require('neo-tree').setup {
      close_if_last_window = true,
      filesystem = {
        filtered_items = {
          visible = true, -- This is what you want: If you set this to `true`, all "hide" just mean "dimmed out"
          hide_dotfiles = false,
          hide_gitignored = true,
        },
        follow_current_file = true,
        group_empty_dirs = true,
        use_libuv_file_watcher = true,
      },
      buffers = {
        follow_current_file = true,
        group_empty_dirs = true,
        show_unloaded = true,
      },
      git_status = {
        symbols = {
          modified = "*",
          untracked = "%",
        },
        window = {
          position = "float",
          mappings = {
            ["A"]  = "git_add_all",
            ["gu"] = "git_unstage_file",
            ["ga"] = "git_add_file",
            ["gr"] = "git_revert_file",
            ["gc"] = "git_commit",
            ["gp"] = "git_push",
            ["gg"] = "git_commit_and_push",
          }
        }
      },
    }
  end,
}
-- vim: ts=2 sts=2 sw=2 et
