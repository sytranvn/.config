local M = {}
M.setup = function()
	local local_vimrc = vim.fn.getcwd() .. '/.nvimrc'
	if vim.loop.fs_stat(local_vimrc) then
		vim.cmd('source ' .. local_vimrc)
	end
	local local_vimrclua = vim.fn.getcwd() .. '/.nvimrc.lua'
	if vim.loop.fs_stat(local_vimrclua) then
		dofile(local_vimrclua)
	end
end
return M
