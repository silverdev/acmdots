;; set up the load path to ~/emacsdir and all subdirs
(if (fboundp 'normal-top-level-add-subdirs-to-load-path)
		(let* ((my-lisp-dir "~/.emacsdir/")
			   (default-directory my-lisp-dir))
		   (setq load-path (cons my-lisp-dir load-path))
		   (normal-top-level-add-subdirs-to-load-path)))

;; Helper macro for safely requiring files with fallback
(defmacro desire (feature filename &optional success failure)
  `(if (require ,feature ,filename t)
	   (eval ,success)
	 (progn (message (format "Failed to load %s" ,filename)) (eval ,failure))))

;; Disable toolbars/menus/etc
(menu-bar-mode -1)
;; tool-bar-mode and scroll-bar-mode are only available for gui emacs
(if window-system
	(progn
	  (tool-bar-mode -1)
	  (scroll-bar-mode -1)))

;; Start the emacs-server for quick startup when using emacsclient
(server-start)

;; Some sane defaults for tabs and column width
(setq-default tab-width 4)
(setq-default fill-column 132)

;; Turn on column numbers
(visual-line-mode 1)
(setq column-number-mode t)

;; backup files should be in ~/.saves
(setq backup-by-copying t
	  backup-directory-alist '(("." . "~/.saves"))
	  delete-old-versions t
	  kept-new-versions 6
	  kept-old-versions 2
	  version-control t)

;; similarly for tramp backups for su and sudo should be in ~/.saves
(setq backup-enable-predicate
	  (lambda (name)
		(and (normal-backup-enable-predicate name)
			 (not
			  (let ((method (file-remote-p name 'method)))
				(when (stringp method)
				  (member method '("su" "sudo"))))))))

;; Mac terminal key support
(if (string= (getenv "TERM_PROGRAM") "Apple_Terminal")
    (progn (global-set-key (kbd "M-[ 5 d") 'backward-word)
		   (global-set-key (kbd "M-[ 5 c") 'forward-word)))

;; C Styling
(setq c-default-style "bsd"
	  c-basic-offset 4)
(add-hook 'c-mode-common-hook '(lambda ()
								 (c-toggle-auto-state 1)))

;; Turn on generic syntax highlighting
(desire 'generic-x "generic-x.el")

;; Turn on line numbering (hopefully with linum-mode)
(if (boundp 'global-linum-mode) 
	(global-linum-mode 1)
	(desire 'linum "linum.el"
			'(global-linum-mode 1)
			'(global-line-number-mode 1)))

;; Set up the color theme
(if (fboundp 'load-theme)
	; We can use emacs24 color themes
	(progn
	  (push "~/.emacsdir/themes/" custom-theme-load-path)
	  (load-theme 'wombat-twilight t))
  ; We can't use modern themes, try to use color-theme package
  (progn
	(message "Emacs24 themes unavailable, falling back to color-theme.el")
	(desire 'color-theme "color-theme.el"
			'(progn (color-theme-initialize) (color-theme-comidia))
			'(if (not (null window-system))
				 (progn
				   (setq initial-frame-alsit '((background-color . "black")
											   (foreground-color . "ghostwhite")))
				   (setq default-frame-alist '((background-color . "black")
											   (foreground-color . "ghostwhite"))))))))

;; Turn on whitespace highlights
(desire 'whitespace "whitespace.el"
		'(progn
		   (setq whitespace-style '(face trailing empty space-before-tab))
		   (global-whitespace-mode)
		   (global-set-key "\C-cw" 'whitespace-cleanup)))

;; Parentheses matching
(desire 'paren "paren.el"
	'(progn
	   (set-face-background 'show-paren-match-face (face-background 'region))
	   (show-paren-mode 1)
	   (setq show-paren-delay 0)
	   (setq show-paren-style "mixed")))

;; Tabs for indentation with spaces for alignment
(desire 'smarttabs "smarttabs.el"
	'(progn
	   (add-hook 'c-mode-hook 'smart-tabs-mode-enable)
	   (smart-tabs-advice c-indent-line c-basic-offset)
	   (smart-tabs-advice c-indent-region c-basic-offset)))

;; load org-mode
(desire 'org-install "org-install.el"
		'(progn
		   (add-to-list 'auto-mode-alist '("\\.org$" . org-mode))
		   (define-key global-map "\C-cl" 'org-store-link)
		   (define-key global-map "\C-ca" 'org-agenda)
		   (setq org-log-done t)
		   (setq org-agenda-files
				 ; Add agendas to this list
				 (list "~/org/personal.org"))))

;; Haskell-Mode
(desire 'haskell-mode "haskell-mode.el"
		'(progn
		   (add-to-list 'auto-mode-alist '("\\.hs$" . haskell-mode))
		   (add-hook 'haskell-mode-hook 'turn-on-haskell-doc-mode)
		   (add-hook 'haskell-mode-hook 'turn-on-haskell-indentation)))

;; rust-mode
(desire 'rust-mode "rust-mode.el")

;; gas-mode replacement for asm-mode
(desire 'gas-mode "gas-mode.el"
		'(add-to-list 'auto-mode-alist '("\\.[sS]$" . gas-mode)))

;; php-mode
(desire 'php-mode "php-mode.el"
		'(progn
		   (add-to-list 'auto-mode-alist '("\\.php$" . php-mode))
		   (add-to-list 'auto-mode-alist '("\\.inc$" . php-mode))))

;; ruby-mode indentation
(add-hook 'ruby-mode-hook '(lambda ()
							 (setq tab-width 2)
							 (setq indent-tab-mode nil)))



;;; Sketchier things that are too specific or need to be cleaned up
(message "Loading sketchier sections of .emacs")

;; android-mode and related
(desire 'android "android.el"
		'(progn
		   (desire 'android-mode "android-mode.el"
				   '(progn
					  (setq android-mode-sdk-dir "/usr/local/Cellar/android-sdk/r9/")
					  (add-hook 'gud-mode-hook
								(lambda()
								  (add-to-list 'gud-jdb-classpath "/usr/local/Cellar/android-sdk/r9/android-10/android.jar")))))))

;; tuareg-mode (better ocaml mode)
(add-to-list 'auto-mode-alist '("\\.ml[iylp]?$" . tuareg-mode))
(autoload 'tuareg-mode "tuareg" "Major mode for editing Caml code." t)
(autoload 'camldebug "camldebug" "Run the Caml debugger" t)

;; Smarter python tabs/spaces
(add-hook 'python-mode-hook (lambda ()
							  (setq tab-width default-tab-width)
							  (python-guess-indent)
							  (if indent-tabs-mode
								  (setq python-indent default-tab-width))))

;; js2-mode (javascript mode)
(add-to-list 'auto-mode-alist '("\\.js(on)?$" . js2-mode))
(autoload 'js2-mode "js2-mode" "Major mode for editing Javascript code." t)

;; processing-mode (A java-mode derivative for the
;; processing java language extension)
(autoload 'processing-mode "processing-mode" "Processing mode" t)
(add-to-list 'auto-mode-alist '("\\.pde$" . processing-mode))
(setq processing-location "/Applications/Processing.app/Contents/MacOS/JavaApplicationStub")
