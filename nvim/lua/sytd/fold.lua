local M = {}

M.setup = function()
	vim.opt.fillchars = { fold = " " }
	vim.opt.foldmethod = "indent"
	vim.opt.foldenable = false
	vim.opt.foldlevel = 99
end
return M
