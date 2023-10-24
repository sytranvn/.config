local M = {}
M.setup = function()
	vim.api.nvim_set_keymap('n', '<leader>m', ':make<CR>', { desc = 'Make' })
end

return M
