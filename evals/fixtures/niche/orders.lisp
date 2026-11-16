; orders.lisp
(defvar counter 0)
(defconstant max-size 100)

(defclass order ()
  ((id :initarg :id :accessor order-id)))

(defun computeTotal (items &optional (tax 0) &key discount &aux (sum 0))
  (dolist (i items)
    (setq sum (+ sum i))
  )
  (* sum (- 1 (or discount 0)) (+ 1 tax))
)

(defun is-valid-order (o)
  (if (order-id o)
      (progn (incf counter) t)))

(defun run-hook (name)
  (eval (list (intern (string-upcase name)))))

(defun total-all (orders)
  (mapcar 'computeTotal orders))

(defun same-amount (a b)
  (eq a b))
