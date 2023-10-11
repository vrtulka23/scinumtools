;;; dip-mode.el --- Syntax highlighter for DIP serialization language. -*- coding: utf-8; lexical-binding: t; -*-

;; Copyright © 2023, by Ondrej Pego Jaura

;; Author: Ondrej Pego Jaura 
;; Version: 1.0.0
;; Created: 5. Oct. 2023
;; Keywords: languages, DIP
;; Homepage: https://github.com/vrtulka23/scinumtools

;; This file is not part of GNU Emacs.

;;; License:

;; You can redistribute this program and/or modify it under the terms of the GNU General Public License version 2.

;;; Commentary:

;; Syntax highlighter for DIP serialization language

(setq dip-font-lock-keywords
      (let* (
            ;; define several category of keywords
            (x-keywords '("true" "false"))
            (x-types '("float" "int" "bool" "str" "table" "float32" "float64" "float128" "int16" "int32" "int64" "uint16" "uint32" "uint64"))
            (x-constants '("$source" "$unit"))
            (x-events '("!options" "!constant" "!format" "!condition" "!tags" "!description"))
            (x-functions '("@case" "@else" "@end"))

            ;; generate regex string for each category of keywords
            (x-keywords-regexp (regexp-opt x-keywords 'words))
            (x-types-regexp (regexp-opt x-types 'words))
            (x-constants-regexp (regexp-opt x-constants 'signs))
            (x-events-regexp (regexp-opt x-events 'signs))
            (x-functions-regexp (regexp-opt x-functions 'signs)))

        `(
          (,x-types-regexp . 'font-lock-type-face)
          (,x-constants-regexp . 'font-lock-constant-face)
          (,x-events-regexp . 'font-lock-builtin-face)
          (,x-functions-regexp . 'font-lock-function-name-face)
          (,x-keywords-regexp . 'font-lock-keyword-face)
          ;; note: order above matters, because once colored, that part won't change.
          ;; in general, put longer words first
          )))

(defface my-number-face
  '((t :foreground "red")) ; You can customize the face attributes as desired
  "Face for highlighting numbers")

;; Highlight numbers and scientific notation in all programming modes
(defun highlight-dip-mode-numbers ()
  "Highlight numbers and scientific notation in all programming modes."
  (font-lock-add-keywords
   nil
   '(("-?\\b[0-9]+\\b\\(?:\\.[0-9]*\\(?:[eE][-+]?[0-9]+\\)?\\)?\\b\\.?" . 'my-number-face))))

;; Add the function to dip modes hooks
(add-hook 'dip-mode-hook 'highlight-dip-mode-numbers)

(defvar dip-mode-syntax-table
  (let ((st (make-syntax-table)))
    (modify-syntax-entry ?{ "<b" st)
    (modify-syntax-entry ?} ">b" st)
    st)
  "Syntax table for dip-mode")

;;;###autoload
(define-derived-mode dip-mode python-mode "dip mode"
  "Major mode for editing LSL (Linden Scripting Language)…"

  ;; code for syntax highlighting
  (setq font-lock-defaults '((dip-font-lock-keywords))))

;; add the mode to the `features' list
(provide 'dip-mode)

;;; dip-mode.el ends here