local M = {}

M.setup = function(config)
	local vim = vim
	local opt = vim.opt
	opt.foldmethod = "expr"
	opt.foldexpr = "nvim_treesitter#foldexpr()"
end

return M
